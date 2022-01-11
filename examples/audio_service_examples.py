"""
This script shows examples of how all the methods in the sensory_cloud.services.audio_service.AudioService class
can be implemented.  The pyaudio package is used to interface with the microphone, which is not built into the
sensory_cloud library, so that must installed in a python environment in addition to sensory_cloud in order to 
run these examples.
"""

import typing
import pyaudio
import multiprocessing
import os
import dotenv

from sensory_cloud.config import Config
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.generated.v1.audio.audio_pb2 import (
    AudioConfig,
    GetModelsResponse,
    TranscribeResponse,
)

from secure_credential_store_example import SecureCredentialStore

dotenv.load_dotenv(override=True)

is_connection_secure = True
is_liveness_enabled = False
device_name = "jhersch-python-sdk-dev"
enrollment_description = "my enrollment"

fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
tenant_id = os.environ.get("TENANT_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
device_id = os.environ.get("DEVICE_ID")
user_id = os.environ.get("USER_ID")
enrollment_id = os.environ.get("AUDIO_ENROLLMENT_ID")
enrollment_group_id = "audio-enrollment-group-id"
event_enrollment_id = "audio-event-enrollment-group-id"


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


def get_audio() -> typing.Tuple[AudioService, AudioConfig, AudioStreamIterator]:
    """
    Helper function to generate AudioService, AudioConfig, and AudioStreamIterator
    objects which will be used in the example functions below.
    """

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


def example_get_models() -> GetModelsResponse:
    """
    Example of retrieving all available audio models to the tenant

    Returns:
        A GetModelsResponse containing information about audio models
    """

    audio_service, audio_config, audio_stream_iterator = get_audio()
    audio_stream_iterator.close()

    return audio_service.get_models()


def example_enroll_with_audio() -> str:
    """
    Example of creating a new audio enrollment with the Open Sesame
    wake word model

    Returns:
        A string containing the the enrollment id if successful, otherwise None
    """

    model_name = "wakeword-16kHz-open_sesame.ubm"

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
        print(
            "Recording enrollment (repeat saying 'Open Sesame' until the enrollment is complete)..."
        )
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
    """
    Example of voice authentication against the Open Sesame wake word model
    created in the example_enroll_with_audio() above

    Returns:
        A boolean denoting whether or not the authentication was successful
    """

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


def example_group_authenticate_with_audio() -> bool:
    """
    Example of voice authentication against the Open Sesame wake word model
    from an enrollment group

    Returns:
        A boolean denoting whether or not the authentication was successful
    """

    audio_service, audio_config, audio_stream_iterator = get_audio()

    authenticate_stream = audio_service.stream_group_authenticate(
        audio_config=audio_config,
        enrollment_group_id=enrollment_group_id,
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


def example_audio_transcription() -> str:
    """
    Example of an audio transcription using the 'vad-lvscr-lights-2.snsr' model

    Returns:
        A string containing a complete transcription
    """

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

    transcription = None
    try:
        print("LVCSR lights session begin\n")
        for response in transcribe_stream:
            if not response.isPartialResult:
                print(response.transcript)
                transcription = response.transcript
        print("Complete transcription detected, ending session")
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        transcribe_stream.cancel()

    return transcription


def example_stream_event() -> str:
    """
    Example of an audio event detected by the 'sound-16kHz-combined-all.trg' model

    Returns:
        A string containing the type of event detected
    """

    event_model = "sound-16kHz-combined-all.trg"
    audio_service, audio_config, audio_stream_iterator = get_audio()

    event_stream = audio_service.stream_event(
        audio_config=audio_config,
        user_id=user_id,
        model_name=event_model,
        audio_stream_iterator=audio_stream_iterator,
    )

    event = None
    try:
        print("Listening for events...")
        for response in event_stream:
            if response.success:
                print(response.resultId)
                event = response.resultId
        print(f"Detected {event}, ending session")
    except Exception as e:
        print(f"Event detection failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        event_stream.cancel()

    return event


def example_create_enrolled_event() -> str:
    """
    Example of creating an enrollment using an enrolled event

    Returns:
        A string containing the new enrollment id
    """

    model_name = "sound-dependent-16kHz.ubm"
    description = "enrolled-event-example"

    audio_service, audio_config, audio_stream_iterator = get_audio()

    enrolled_event_stream = audio_service.stream_create_enrolled_event(
        audio_config=audio_config,
        description=description,
        user_id=user_id,
        model_name=model_name,
        audio_stream_iterator=audio_stream_iterator,
    )

    enrollment_id = None
    try:
        print("Enrolling...")
        percent_complete = 0
        print(f"percent complete = {percent_complete}")
        for response in enrolled_event_stream:
            if response.percentComplete != percent_complete:
                percent_complete = response.percentComplete
                print(f"percent complete = {percent_complete}")
            if response.percentComplete >= 100:
                break
            enrollment_id = response.enrollmentId
        print("Enrollment complete!")
        print(f"Enrollment Id = {enrollment_id}")
    except Exception as e:
        print(f"Enrolled event failed with error: {str(e)}")
    finally:
        audio_stream_iterator.close()
        enrolled_event_stream.cancel()

    return enrollment_id


def example_validate_enrolled_event() -> bool:
    """
    Example validating against the enrollment created in example_create_enrolled_event()

    Returns:
        A boolean denoting whether or not the validation was successful
    """

    audio_service, audio_config, audio_stream_iterator = get_audio()

    validate_enrolled_event_stream = audio_service.stream_validate_enrolled_event(
        audio_config=audio_config,
        enrollment_id=event_enrollment_id,
        audio_stream_iterator=audio_stream_iterator,
    )

    authentication_success = True
    try:
        print("Authenticating enrolled event...")
        for response in validate_enrolled_event_stream:
            if response.success:
                authentication_success = True
                break
        print("Authentication successful!\n")
    except Exception as e:
        print(f"Enrolled event validation failed with error: {str(e)}")
    finally:
        audio_stream_iterator.close()
        validate_enrolled_event_stream.cancel()

    return authentication_success


def example_group_validate_enrolled_event():
    """
    Example validating against the enrollment group containing the event enrollment created in
    example_create_enrolled_event()

    Returns:
        A boolean denoting whether or not the validation was successful
    """

    audio_service, audio_config, audio_stream_iterator = get_audio()

    validate_enrolled_event_stream = audio_service.stream_group_validate_enrolled_event(
        audio_config=audio_config,
        enrollment_group_id=enrollment_group_id,
        audio_stream_iterator=audio_stream_iterator,
    )

    authentication_success = True
    try:
        print("Authenticating enrolled event...")
        for response in validate_enrolled_event_stream:
            if response.success:
                authentication_success = True
                break
        print("Authentication successful!\n")
    except Exception as e:
        print(f"Enrolled event validation failed with error: {str(e)}")
    finally:
        audio_stream_iterator.close()
        validate_enrolled_event_stream.cancel()

    return authentication_success
