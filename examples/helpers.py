import os
import typing
import pyaudio
import time
import cv2
import configparser
import multiprocessing
from io import BytesIO
from PIL import Image

from sensory_cloud.config import Config, CloudHost
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.initializer import FileSystemCredentialStore

from sensory_cloud.services.video_service import VideoService
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.services.management_service import ManagementService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2

from secure_credential_store_example import SecureCredentialStore


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
device_info_path = os.path.dirname(config_path)

environment_config = configparser.ConfigParser()
environment_config.read(config_path)


def get_oauth_service() -> OauthService:
    """
    Function the creates an OauthService object using the credentials set in
    config.json

    Returns:
        An OauthService object
    """

    cloud_host: CloudHost = CloudHost(
        host=environment_config.get("SDK-configuration", "fullyQualifiedDomainName"),
        is_connection_secure=environment_config.getboolean(
            "SDK-configuration", "isSecure"
        ),
    )
    config: Config = Config(
        cloud_host=cloud_host,
        tenant_id=environment_config.get("SDK-configuration", "tenantId"),
    )
    config.connect()

    credential_store: SecureCredentialStore = SecureCredentialStore(
        client_id=environment_config.get("client-configuration", "clientId"),
        client_secret=environment_config.get("client-configuration", "clientSecret"),
    )

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )

    return oauth_service


def get_token_manager() -> TokenManager:
    """
    Function that creates a TokenManager object using the credentials set in
    config.json

    Returns:
        A TokenManager object
    """

    oauth_service: OauthService = get_oauth_service()

    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

    return token_manager


class AudioStreamIterator:
    """
    This is a sample audio stream iterator that uses the pyaudio package to interface with
    the microphone and can be used with all of the methods in the AudioService class except for
    get_models().  This implementation of an audio stream iterator is just one option, but the user
    has the freedom to choose whatever implementation they would like, so long as it is an iterator that yields
    audio bytes.
    """

    _p_output, _p_input = multiprocessing.Pipe()

    def __init__(
        self,
        channels: int,
        rate: int,
        frames_per_buffer: int,
        format: int = pyaudio.paInt16,
        post_processing: audio_pb2.AudioPostProcessingAction = None,
    ):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._py_audio = pyaudio.PyAudio()
        self._stream = self._py_audio.open(
            format=format,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=frames_per_buffer,
            stream_callback=self._record_callback,
        )
        self._post_processing = post_processing

    def _record_callback(self, in_data, count, time_info, status):
        self._p_input.send(in_data)
        return (None, pyaudio.paContinue)

    def __iter__(self):
        return self

    def __next__(
        self,
    ) -> typing.Tuple[bytes, audio_pb2.AudioRequestPostProcessingAction]:
        _next = (
            self._p_output.recv(),
            audio_pb2.AudioRequestPostProcessingAction(action=self._post_processing),
        )
        return _next

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self._py_audio.terminate()


class VideoStreamIterator:
    """
    Sample iterator class that uses opencv to interface with the device camera
    and return a stream of image bytes from the video recording
    """

    def __init__(self, frame_rate: int = 1):
        self._camera = cv2.VideoCapture(0)
        if frame_rate is not None:
            self._delay = 1 / frame_rate
        else:
            self._delay = 0

    def __iter__(self):
        return self

    def __next__(self):
        success, frame = self._camera.read()
        if success:
            time.sleep(self._delay)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            buffer = BytesIO()
            Image.fromarray(frame).save(buffer, format="JPEG", quality=95)
            return buffer.getvalue()
        else:
            raise StopIteration

    def close(self):
        self._camera.release()


def get_audio_service() -> AudioService:
    """
    Function that creates an AudioService object using the credentials set
    in config.json

    Returns:
        An AudioService object
    """

    token_manager: TokenManager = get_token_manager()

    audio_service: AudioService = AudioService(
        config=token_manager.oauth_service._config, token_manager=token_manager
    )

    return audio_service


def get_audio_config(sample_rate_hertz: int = 16000) -> audio_pb2.AudioConfig:
    """
    Function that creates an audio_pb2.AudioConfig object with
    Linear 16 encoding, one audio channel, 16 KHz sample rate, and
    uses US english

    Returns:
        An audio_pb2.AudioConfig object
    """

    audio_config: audio_pb2.AudioConfig = audio_pb2.AudioConfig(
        encoding=audio_pb2.AudioConfig.AudioEncoding.Value("LINEAR16"),
        audioChannelCount=1,
        sampleRateHertz=sample_rate_hertz,
        languageCode="en-US",
    )

    return audio_config


def get_audio_stream_iterator(
    audio_config: audio_pb2.AudioConfig,
) -> AudioStreamIterator:
    """
    Function that creates an AudioStreamIterator object with an
    upload interval of 100 ms

    Returns:
        An AudioStreamIterator object
    """

    upload_interval: int = 100  # (ms)
    frames_per_buffer: int = int(
        audio_config.sampleRateHertz * (upload_interval / 1000)
    )

    audio_stream_iterator: AudioStreamIterator = AudioStreamIterator(
        channels=audio_config.audioChannelCount,
        rate=audio_config.sampleRateHertz,
        frames_per_buffer=frames_per_buffer,
    )

    return audio_stream_iterator


def get_video_service() -> VideoService:
    """
    Function that creates a VideoService object using the
    credentials set in config.json

    Returns:
        A VideoService object
    """

    token_manager: TokenManager = get_token_manager()

    video_service: VideoService = VideoService(
        config=token_manager.oauth_service._config, token_manager=token_manager
    )

    return video_service


def get_management_service() -> ManagementService:
    """
    Function that creates a ManagementService object using the
    credentials set in config.json

    Returns:
        A ManagementService object
    """

    token_manager: TokenManager = get_token_manager()

    management_service: ManagementService = ManagementService(
        config=token_manager.oauth_service._config, token_manager=token_manager
    )

    return management_service


def get_device_id() -> str:
    """
    Function that first checks environment variables for the device id.
    If the device id is not set as an environment variable then the device information
    will be retrieved from the root directory of this project.
    """

    device_id = os.environ.get("SENSORYCLOUD_DEVICE_ID")
    if device_id is None:
        keychain = FileSystemCredentialStore(
            root_path=os.path.dirname(os.path.abspath(__file__))
        )
        if "deviceID" in keychain:
            device_id = keychain["deviceID"]
        else:
            error_string = """The device id is not stored as an environment variable or in the root directory of this project.
            Make sure you have run the registration_examples.py script to set the device id."""
            raise Exception(error_string)

    return device_id
