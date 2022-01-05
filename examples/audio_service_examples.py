import sys
import typing
import pyaudio
import multiprocessing
import os
import dotenv

from sensory_cloud.config import Config
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.generated.v1.audio.audio_pb2 import AudioConfig, TranscribeResponse

from secure_credential_store_example import SecureCredentialStore

dotenv.load_dotenv(override=True)

is_connection_secure = True
is_liveness_enabled = False
model_name = "wakeword-16kHz-open_sesame.ubm"
device_name = "jhersch-python-sdk-dev"
enrollment_description = "my enrollment"

fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
tenant_id = os.environ.get("TENANT_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
device_id = os.environ.get("DEVICE_ID")
device_credential = os.environ.get("DEVICE_CREDENTIAL")
user_id = os.environ.get("USER_ID")
enrollment_id = os.environ.get("AUDIO_ENROLLMENT_ID")


class AudioStreamIterator:
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


def get_audio() -> typing.Tuple[AudioService, AudioConfig, AudioStreamIterator]:

    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name,
        is_connection_secure=is_connection_secure,
        tenant_id=tenant_id,
    )
    config.connect()

    cred_store = SecureCredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    audio_service = AudioService(config, token_manager)

    audio_config = AudioConfig(
        encoding=AudioConfig.AudioEncoding.Value("LINEAR16"),
        audioChannelCount=1,
        sampleRateHertz=16000,
        languageCode="en-US",
    )

    upload_interval = 100  # (ms)
    frames_per_buffer = int(audio_config.sampleRateHertz * (upload_interval / 1000))

    audio_stream_iterator = AudioStreamIterator(
        channels=audio_config.audioChannelCount,
        rate=audio_config.sampleRateHertz,
        frames_per_buffer=frames_per_buffer,
    )

    return audio_service, audio_config, audio_stream_iterator


def example_enroll_with_audio() -> str:

    audio_service, audio_config, audio_stream_iterator = get_audio()

    enrollment_stream = audio_service.stream_enrollment(
        audio_config=audio_config,
        description=enrollment_description,
        user_id=user_id,
        device_id=device_id,
        model_name=model_name,
        is_liveness_enabled=is_liveness_enabled,
        audio_stream_iterator=audio_stream_iterator,
    )

    enrollment_id = None
    try:
        print("Recording enrollment...")
        percent_complete = 0
        print(f"percent complete = {percent_complete}")
        for response in enrollment_stream:
            if response.percentComplete != percent_complete:
                percent_complete = response.percentComplete
                print(f"percent complete = {percent_complete}")
            if response.percentComplete >= 100:
                break
        enrollment_id = response.enrollmentId
        print("Enrollment complete!")
        print(f"Enrollment Id = {enrollment_id}")
    except Exception as e:
        print(f"Enrollment failed with error: {str(e)}")
    finally:
        audio_stream_iterator.close()
        enrollment_stream.cancel()

    return enrollment_id


def example_authenticate_with_audio() -> bool:

    audio_service, audio_config, audio_stream_iterator = get_audio()

    authenticate_stream = audio_service.stream_authenticate(
        audio_config=audio_config,
        enrollment_id=enrollment_id,
        is_liveness_enabled=is_liveness_enabled,
        audio_stream_iterator=audio_stream_iterator,
    )

    authentication_success = False
    try:
        print("Authenticating for pass phrase 'Open Sesame'...")
        for response in authenticate_stream:
            if response.success:
                authentication_success = True
                break
        print("Authentication successful!\n")
    except Exception as e:
        print(f"Authentication failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        authenticate_stream.cancel()

    return authentication_success


def example_audio_transcription() -> typing.List[str]:
    transcription_model = "vad-lvscr-lights-2.snsr"
    audio_service, audio_config, audio_stream_iterator = get_audio()

    transcribe_stream: typing.Iterable[
        TranscribeResponse
    ] = audio_service.stream_transcription(
        audio_config=audio_config,
        user_id=user_id,
        model_name=transcription_model,
        audio_stream_iterator=audio_stream_iterator,
    )

    transcriptions: typing.List[str] = []
    try:
        print("LVCSR lights session begin\n")
        for response in transcribe_stream:
            if response.transcript == "help":
                cmd = "'Help' is the exit command for this demo, so ending session..."
                print(f"{cmd}\n")
                transcriptions.append(response.transcript)
                break
            if not response.isPartialResult:
                print(response.transcript)
                transcriptions.append(response.transcript)
        print("Session end")
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        transcribe_stream.cancel()

    return transcriptions


def example_audio_event():
    event_model = "sound-16kHz-combined-all.trg"
    audio_service, audio_config, audio_stream_iterator = get_audio()

    event_stream = audio_service.stream_event(
        audio_config=audio_config,
        user_id=user_id,
        model_name=event_model,
        audio_stream_iterator=audio_stream_iterator,
    )

    events = []
    try:
        print("Listening for events...")
        for response in event_stream:
            if response.success:

                events.append(response)
                print(response.resultId, response.score)

                if response.resultId == "Door Knock":
                    print(
                        "A door knock detection is the exit signal for this demo, so ending session..."
                    )
                    break
        print("Session end")
    except Exception as e:
        print(f"Event detection failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        event_stream.cancel()

    return events


if __name__ == "__main__":
    if example_authenticate_with_audio():
        transcriptions = example_audio_transcription()
