# Python SDK
Sensory Cloud is built using python 3.8, but it is compatible with python 3.6 and higher

## General Information
Before getting started, you must spin up a Sensory Cloud inference server or have Sensory spin one up for you. You must also have the following pieces of information:
- Your inference server URL (fully_qualified_domain_name)
- Your Sensory Tenant ID (UUID)
- Your configured secret key (device_credential) used to register OAuth clients and devices

## Checking Server Health
It's important to check the health of your Sensory Inference server. You can do so by following the example [here](examples/health_service_examples.py).

## Secure Credential Store
ISecureCredential is an interface that store and serves your OAuth credentials (client_id and client_secret).
The `client_id` must be a uuid and the `client_secret` can be generated using the CryptoService as shown below.

```
import uuid
from sensory_cloud.services.crypto_service import CryptoService

client_id = str(uuid.uuid4())
client_secret = CryptoService().get_secure_random_string(length=24) # This will yield a client secret with 24 characters
```

You will want to store your client credentials in a safe place.  The examples used throughout this README store credentials in a `.env` file in
the examples subdirectory and are retrieved using the [`python-dotenv`](https://pypi.org/project/python-dotenv/) package which is not a dependency
of the `sensory-cloud` library so these examples must be run in a python environment with both packages installed if you want to run the example code
directly.

ISecureCredential must be implemented by you and follow the patterns of the abstract ISecureCredential class defined in the
in the [oauth_service.py](src/sensory_cloud/services/oauth_service.py) file.
The credentials should be persisted in a secure manner, such as in an encrypted database.
OAuth device credentials should be generated one time per unique machine.
A crude example of ISecureCredential can be seen [here](examples/secure_credential_store_example.py).

## Registering OAuth Credentials
OAuth credentials should be registered once per unique machine and is the first step that must be taken in order to create enrollments. 
Registration is very simple, and provided as part of the SDK.
The source code for the OAuthService can be found in the [oauth_service.py](src/sensory_cloud/services/oauth_service.py) file and
the example file [here](examples/oauth_service_examples.py) shows how to create an OAuthService and register a device for the first time.
Similar to the `client_id` and `client_secret`, the `device_id` and `device_name` (which are strings set by the user) 
should be safely stored and easily retrievable.  As mentioned,
the examples store this information in a `.env` file located in the examples subdirectory.  To follow the examples directly, you should have a 
the following environment variables set in a `.env` file or in your `.bash_profile` if using MacOS or your `.bashrc` if using Linux.

```
export FULLY_QUALIFIED_DOMAIN_NAME="my.inference.server.url.com"
export TENANT_ID="my-uuid-tenant-id"
export DEVICE_CREDENTIAL="my-configured-secret-key"

export CLIENT_ID="my-uuid-client-id"
export CLIENT_SECRET="my-client-secret"

export DEVICE_ID="my-new-device-id"
export DEVICE_NAME-"my-new-device-name"
```


## Creating a Token Manager
The TokenManger class handles requesting OAuth tokens when necessary.  
The source code for the TokenManager can be found in the [token_manager.py](src/sensory_cloud/token_manager.py) and
an example of its implementation can be seen [here](examples/token_manager_example.py).


## Creating an Audio Service
The code snippets shown in this section give a brief summary of the implementation of the `AudioService` class.  Full examples can be found
[here](examples/audio_service_examples.py) and the source code for the AudioService class can be found in the 
[audio_service.py](src/sensory_cloud/services/audio_service.py) file.

AudioService provides methods to stream audio to Sensory Cloud. It is recommended to only have 1 instance of AudioService
instantiated per Config. In most circumstances you will only ever have one Config, unless your app communicates with
multiple Sensory Cloud servers.

```
def get_audio_service() -> AudioService:
    is_connection_secure: bool = True
    fully_qualifiied_domain_name: str = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
    tenant_id: str = os.environ.get("TENANT_ID")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")

    config: Config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name,
        is_connection_secure=is_connection_secure,
        tenant_id=tenant_id,
    )
    config.connect()

    cred_store: SecureCredentialStore = SecureCredentialStore(client_id, client_secret)
    oauth_service: OauthService = OauthService(config=config, secure_credential_store=cred_store)

    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

    audio_service: AudioService = AudioService(config, token_manager)

    return audio_service
```

### Obtaining Audio Models
Certain audio models are available to your application depending on the models that are configured for your instance of Sensory Cloud.
In order to determine which audio models are accessible to you, you can execute the below code.

```
audio_service: AudioService = get_audio_service()
audio_models: GetModelsResponse = audio_service.get_models()
```

Audio models contain the following properties:

- name - the unique name tied to this model. Used when calling any other audio function.
- isEnrollable - indicates if the model can be enrolled into. Models that are enrollable can be used in the CreateEnrollment function.
- modelType - indicates the class of model and it's general function.
- fixedPhrase - for speech-based models only. Indicates if a specific phrase must be said.
- samplerate - indicates the audio samplerate required by this model. Generally, the number will be 16000.
- isLivenessSupported - indicates if this model supports liveness for enrollment and authentication. Liveness provides an added layer of security by requring a users to speak random digits.

### Enrolling with Audio
In order to enroll with audio, you must first ensure you have an enrollable model enabled for your Sensory Cloud instance. This can be obtained via the GetModels() request.
Enrolling with audio uses an audio stream iterator that yields audio bytes. A sample audio stream iterator is shown below and passed into the audio enrollmnent class method. 
It is important to save the enrollmentId in order to perform authentication against it in the future.

NOTE: The snippet below and the audio service [examples](examples/audio_service_examples.py) file use the [`pyaudio`](https://pypi.org/project/PyAudio/)
package to create the AudioStreamIterator.  The `pyaudio` package is not a dependancy of the `sensory-cloud` library so it must be installed seperately 
if you want to follow the example code directly.
```
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

description = "my enrollment description"
user_id = "my-user-id"
device_id = os.environ.get("DEVICE_ID")

audio_service: AudioService = get_audio_service()

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

enrollment_stream = audio_service.stream_enrollment(
    audio_config=audio_config,
    description=enrollment_description,
    user_id=user_id,
    device_id=device_id,
    model_name="my-audio-enrollment-model",
    is_liveness_enabled=is_liveness_enabled,
    audio_stream_iterator=audio_stream_iterator,
)

enrollment_id = None
try:
    print(
        "Recording enrollment (repeat saying the model enrollment utterance until the enrollment is complete)..."
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
```

The `enrollment_id` generated by the code snippet above or from running the example_enroll_with_audio() in the [audio_service_examples.py](examples/audio_service_examples.py) file
should be stored as an environment variable called `AUDIO_ENROLLMENT_ID` to be used in the example_authenticate_with_audio() which is discussed next.

### Authenticating with Audio
Authenticating with audio is similar to enrollment, except now you have an enrollment_id to pass into the function.  The AudioStreamIterator
class shown in the enrollment example above will be used again here.

```
is_liveness_enabled = False

audio_service: AudioService = get_audio_service()

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

authenticate_stream = audio_service.stream_authenticate(
    audio_config=audio_config,
    enrollment_id=os.environ.get("AUDIO_ENROLLMENT_ID"),
    is_liveness_enabled=is_liveness_enabled,
    audio_stream_iterator=audio_stream_iterator,
)

authentication_success = False
try:
    print("Authenticating...")
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
```

### Audio Events
Audio events are used to recognize specific words, phrases, or sounds.

The below example waits for a single event to be recognized and ends the stream.

```
event_model = "my-audio-event-model"

audio_service: AudioService = get_audio_service()

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
```

### Create Enrolled Event
You can enroll your own event into the Sensory cloud system. The process is similar to biometric enrollment where you must
play a sound or speak a particular phrase 4 or more times. This is usefull for recognizing sounds that are not offered by Sensory Cloud.

```
model_name = "my-enrolled-event-model"
description = "enrolled-event-example"

audio_service: AudioService = get_audio_service()

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
```

### Validate Enrolled Event
Once you've created an enroled event, you can listen for that event (or groups of events) by calling
the ValidateEnrolledEvent function.

```
audio_service: AudioService = get_audio_service()

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
```

### Transcription
Transcription is used to convert audio into text.

```
transcription_model = "my-transcription-model"

audio_service: AudioService = get_audio_service()

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
```

## Creating a Video Service
VideoService provides methods to stream images to Sensory Cloud. It is recommended to only have 1 instance of VideoService
instantiated per Config. In most circumstances you will only ever have one Config, unless your app communicates with
multiple Sensory Cloud servers.

The snippets below give a brief summary of the implementation of the VideoService class.  The source code can be seen in the
[video_service.py](src/sensory_cloud/services/video_service.py) and full examples of its implementation are given 
[here](examples/video_service_examples.py).

```
def get_video_service() -> VideoService:
    is_connection_secure = True
    fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
    tenant_id = os.environ.get("TENANT_ID")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")

    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name,
        is_connection_secure=is_connection_secure,
        tenant_id=tenant_id,
    )
    config.connect()

    cred_store = SecureCredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    video_service = VideoService(config=config, token_manager=token_manager)

    return video_service
```

### Obtaining Video Models
Certain video models are available to your application depending on the models that are configured for your instance of Sensory Cloud.
In order to determine which video models are accessible to you, you can execute the below code.

```
video_service: VideoService = get_video_service()
video_models: GetModelsResponse = video_service.get_models()
```

Video models contain the following properties:

- name - the unique name tied to this model. Used when calling any other video function.
- isEnrollable - indicates if the model can be enrolled into. Models that are enrollable can be used in the CreateEnrollment function.
- modelType - indicates the class of model and it's general function.
- fixedObject - for recognition-based models only. Indicates if this model is built to recognize a specific object.
- isLivenessSupported - indicates if this model supports liveness for enrollment and authentication. Liveness provides an added layer of security.

### Enrolling with Video
In order to enroll with video, you must first ensure you have an enrollable model enabled for your Sensory Cloud instance. This can be obtained via the GetModels() request.
Enrolling with video uses a call and response streaming pattern to allow immediate feedback to the user during enrollment.  Enrolling with video uses a video stream iterator that yields image bytes. A sample video stream iterator is shown below and passed into the video enrollmnent class method. It is important to save the enrollmentId in order to perform authentication against it in the future.

NOTE:  The snippet below and the video service [examples](examples/video_service_examples.py) use the [`opencv-python`](https://pypi.org/project/opencv-python/)
package to interface with the device camera in the VideoStreamIterator class defined below.  The `opencv-python` package is not a dependency of the `sensory-cloud`
library and must be installed seperately to follow the example code directly.

```
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


model_name: str = "face_recognition_mathilde"
enrollment_description: str = "jhersch-video-enrollment-cpu"

device_id: str = os.environ.get("DEVICE_ID")
user_id: str = os.environ.get("USER_ID")

video_service: VideoService = get_video_service()

video_stream_iterator: VideoStreamIterator = VideoStreamIterator()

enrollment_stream = video_service.stream_enrollment(
    description=enrollment_description,
    user_id=user_id,
    device_id=device_id,
    model_name=model_name,
    is_liveness_enabled=is_liveness_enabled,
    video_stream_iterator=video_stream_iterator,
)

print("Recording enrollment...")
percent_complete = 0
enrollment_id = None
try:
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
    f"Enrollment failed with error: {str(e)}"
finally:
    video_stream_iterator.close()
    enrollment_stream.cancel()
```

The `enrollment_id` generated by the code snippet above or from running the example_enroll_with_video() in the [video_service_examples.py](examples/video_service_examples.py) file
should be stored as an environment variable called `VIDEO_ENROLLMENT_ID` to be used in the example_authenticate_with_audio() which is discussed next.

### Authenticating with Video
Authenticating with video is similar to enrollment, except now you have an enrollmentId to pass into the function.

```
enrollment_id: str = os.environ.get("VIDEO_ENROLLMENT_ID")

video_service: VideoService = get_video_service()

video_stream_iterator: VideoStreamIterator = VideoStreamIterator()

authenticate_stream = video_service.stream_authentication(
    enrollment_id=enrollment_id,
    is_liveness_enabled=False,
    video_stream_iterator=video_stream_iterator,
)

success: bool = False
try:
    print("Authenticating...")
    for response in authenticate_stream:
        print(response.success)
        if response.success:
            success = True
            break
    print("Authentication successful!")
except Exception as e:
    print(f"Authentication failed with error {str(e)}")
finally:
    video_stream_iterator.close()
    authenticate_stream.cancel()
```

### Video Liveness
Video Liveness allows one to send images to Sensory Cloud in order to determine if the subject is a live individual rather than a spoof, such as a paper mask or picture.

```
model_name: str = "my-recognition-model"
user_id: str = os.environ.get("USER_ID")

video_service: VideoService = get_video_service()

video_stream_iterator: VideoStreamIterator = VideoStreamIterator()

recognition_stream = video_service.stream_liveness_recognition(
    user_id=user_id,
    model_name=model_name,
    video_stream_iterator=video_stream_iterator,
)

alive = False
try:
    print("Running liveness recognition...")
    for response in recognition_stream:
        print(response.isAlive)
        if response.isAlive:
            alive = True
            break
    print("You're alive!")
except Exception as e:
    print(f"Liveness recognition failed with error {str(e)}")
finally:
    video_stream_iterator.close()
    recognition_stream.cancel()
```

### Creating a Management Service
The ManagementService is used to manage typical CRUD operations with Sensory Cloud, such as deleting enrollments or creating enrollment groups.
For more information on the specific methods of the ManagementService, please refer to the [management_service.py](src/sensory_cloud/services/management_service.py) file.
The example file [here](examples/management_service_examples.py) shows how to create a ManagementService object.