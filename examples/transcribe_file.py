import wave
import threading
import configparser
from queue import Queue

from sensory_cloud.services.audio_service import AudioService, TranscriptAggregator
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.config import Config, CloudHost
from sensory_cloud.services.oauth_service import ISecureCredentialStore

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


config_path = "/Users/jhersch/Documents/code/sdks/python-sdk/examples/config.ini"

environment_config = configparser.ConfigParser()
environment_config.read(config_path)


class SecureCredentialStore(ISecureCredentialStore):
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret


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


class FileTranscriptionIterator:
    transcript = None
    responses = []
    _queue = Queue()
    _stop_event = threading.Event()

    def __init__(self):
        self._stop_event.set()

    def __iter__(self):
        return self

    def __next__(self):
        if self._stop_event.is_set():
            post_processing_action = None
            item = self._queue.get()
            self._queue.task_done()
            if item == "stop":
                post_processing_action = audio_pb2.AudioRequestPostProcessingAction(
                    action=audio_pb2.AudioPostProcessingAction.FINAL
                )
                item = b""
                self.stop()
            _next = (item, post_processing_action)
            return _next
        raise StopIteration

    def put(self, item):
        self._queue.put(item)

    def stop(self):
        self._stop_event.clear()


def example_wave_file_transcription(file_path: str) -> str:
    """
    Example of an audio transcription using the 'speech_recognition_en' speech
    to text model.  This function will read in a wave file and return the
    transcription as a string.

    Args:
        file_path: path to wave file to be transcribed

    Returns:
        A string containing a complete transcription
    """

    frames_per_buffer: int = 1024

    transcription_iterator: FileTranscriptionIterator = FileTranscriptionIterator()

    with wave.open(file_path, "rb") as wave_file:
        buffer: bytes = wave_file.readframes(frames_per_buffer)
        while buffer != b"":
            transcription_iterator.put(buffer)
            buffer: bytes = wave_file.readframes(frames_per_buffer)

    for _ in range(50000):
        transcription_iterator.put(b"0")

    transcription_iterator.put("stop")

    transcription_model: str = "speech_recognition_en"

    audio_service: AudioService = get_audio_service()
    audio_config: audio_pb2.AudioConfig = get_audio_config()

    transcribe_stream = audio_service.stream_transcription(
        audio_config=audio_config,
        user_id=environment_config.get("examples-configuration", "userId"),
        model_name=transcription_model,
        enable_punctuation_capitalization=True,
        audio_stream_iterator=transcription_iterator,
    )

    transcript_aggregator: TranscriptAggregator = TranscriptAggregator()

    try:
        print("Transcription session begin ...")
        for response in transcribe_stream:
            transcript_aggregator.process_response(response)
            full_transcript = transcript_aggregator.get_transcript()
            transcription_iterator.transcript = full_transcript
            transcription_iterator.responses.append(response)
        print("Transcription complete, ending session")
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}")
    finally:
        transcribe_stream.cancel()

    transcript: str = transcript_aggregator.get_transcript()

    return transcript


if __name__ == "__main__":
    file_transcript: str = example_wave_file_transcription(
        "/Users/jhersch/Desktop/kadri/audio47ac2tco.wav"
    )
