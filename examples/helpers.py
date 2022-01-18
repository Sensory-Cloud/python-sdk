import json
import pyaudio
import cv2
import multiprocessing
from io import BytesIO
from PIL import Image

from sensory_cloud.config import Config
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.services.video_service import VideoService
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.services.management_service import ManagementService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2

from secure_credential_store_example import SecureCredentialStore


with open("config.json", "r") as config_file:
    environment_config: dict = json.load(config_file)


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

    def _record_callback(self, in_data, count, time_info, status):
        self._p_input.send(in_data)
        return (None, pyaudio.paContinue)

    def __iter__(self):
        return self

    def __next__(self):
        return self._p_output.recv()

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self._py_audio.terminate()


def get_audio_service() -> AudioService:

    config: Config = Config(
        fully_qualifiied_domain_name=environment_config["fully_qualified_domain_name"],
        tenant_id=environment_config["tenant_id"],
    )
    config.connect()

    credential_store: SecureCredentialStore = SecureCredentialStore(
        client_id=environment_config["client_id"],
        client_secret=environment_config["client_secret"],
    )

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )

    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

    audio_service: AudioService = AudioService(
        config=config, token_manager=token_manager
    )

    return audio_service


def get_audio_config() -> audio_pb2.AudioConfig:

    audio_config: audio_pb2.AudioConfig = audio_pb2.AudioConfig(
        encoding=audio_pb2.AudioConfig.AudioEncoding.Value("LINEAR16"),
        audioChannelCount=1,
        sampleRateHertz=16000,
        languageCode="en-US",
    )

    return audio_config


def get_audio_stream_iterator(
    audio_config: audio_pb2.AudioConfig,
) -> AudioStreamIterator:

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


class VideoStreamIterator:
    def __init__(self):
        self._camera = cv2.VideoCapture(0)

    def __iter__(self):
        return self

    def __next__(self):
        success, frame = self._camera.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            buffer = BytesIO()
            Image.fromarray(frame).save(buffer, format="JPEG", quality=95)
            return buffer.getvalue()
        else:
            raise StopIteration

    def close(self):
        self._camera.release()


def get_video_service() -> VideoService:

    config: Config = Config(
        fully_qualifiied_domain_name=environment_config["fully_qualified_domain_name"],
        tenant_id=environment_config["tenant_id"],
    )
    config.connect()

    credential_store: SecureCredentialStore = SecureCredentialStore(
        client_id=environment_config["client_id"],
        client_secret=environment_config["client_secret"],
    )

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )

    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

    video_service: VideoService = VideoService(
        config=config, token_manager=token_manager
    )

    return video_service


def get_management_service() -> ManagementService:

    config: Config = Config(
        fully_qualifiied_domain_name=environment_config["fully_qualified_domain_name"],
        tenant_id=environment_config["tenant_id"],
    )
    config.connect()

    credential_store: SecureCredentialStore = SecureCredentialStore(
        client_id=environment_config["client_id"],
        client_secret=environment_config["client_secret"],
    )

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )

    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

    management_service: ManagementService = ManagementService(
        config=config, token_manager=token_manager
    )

    return management_service
