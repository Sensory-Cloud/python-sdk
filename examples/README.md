# Sensory Cloud Python SDK Examples

## Python Environment
The Sensory Cloud python SDK is supported for python >= 3.6.  Before running the examples described below, the following packages must be
installed:

```
pip install sensory-cloud
pip install Wave
pip install PyAudio
pip install opencv-python
pip install Pillow
```

## Setting Up Configuration Parameters
Before starting with these examples you will need to create an ini config file called `config.ini`  in this directory as shown below.

```
[SDK-configuration]
fullyQualifiedDomainName = my.unique.domain.com                                 # Obtained from Sensory
tenantId = my-tenant-id                                                         # Obtained from Sensory
credential = my-credential                                                      # Obtained from Sensory
enrollmentType = none, jwt, or sharedSecret                                     # Selected by user
isSecure = True or False                                                        # Selected by user

[examples-configuration]
userId = my-user-name                                                           # Selected by user
```

As seen, there should initially be two sections in the config file - `SDK-configuration` and `examples-configuration`.  The `SDK-configuration` will
not change but additional variables containing enrollment ids will be added to the `examples-configuration` section once the `enrollment_examples.py` 
script is successfully run and an additional section called `client-configuration` with `clientId` and `clientSecret` fields will be added once the
`registration_examples.py` script is successfully run.

The `fullyQualifiedDomainName`, `tenantId`, and `credential` are obtained from Sensory upon registration and those credentials should
be placed in the `config.ini` file.  The `enrollmentType`, `isSecure`, and `userId` values are selected by the user.  
The remaining configuration parameters will be set as we work through the registration and enrollment examples.

## Device Credentials
The two device credentials used are `deviceId` and `deviceName`.  These two values can bet set and retrieved in one of two ways.  The first way is 
to set them as environment variables with the following keys:

- SENSORYCLOUD_DEVICE_ID
- SENSORYCLOUD_DEVICE_NAME

The sdk will look for these environment variable keys first when finding device credentials.  The second option is to store the device credentials
on disk.  If the device credentials are not present as environment variables then the sdk will look for them as files called `sensory-cloud.deviceID` and
`sensory-cloud.deviceName`.  If you run the `registration_examples.py` script, then that script will look for the device credential files in this examples
subdirectory.  If you want to store the device info on disk but in another location, you can edit the `device_info_path` on line 26 of the `helpers.py` file.  If the device credentials are not present in the `device_info_path` and they are not environment variables, then the `registration_examples.py` script will generate random uuids for
each credential and store them in the `device_info_path`.

## Helpers
The `helpers.py` file has several helper functions that are used throughout the examples discussed below.  For example,
the `helpers.py` defines the AudioStreamIterator class which interfaces with your device microphone and the VideoStreamIterator class that
interfaces with your device camera.  There are also helper functions that create instances of the AudioService, VideoService, and ManagementService
which are used frequently.

## Registration
The first step in using the Sensory Cloud Python SDK is to setup client credentials and register your device.  An example of this process is covered
in `registration_examples.py`.  After running the registration examples, the `client-configuration` section in
the `config.ini` file should be populated.  It should look something like this:
```
[SDK-configuration]
fullyQualifiedDomainName = my.unique.domain.com                                 # Obtained from Sensory
tenantId = my-tenant-id                                                         # Obtained from Sensory
credential = my-credential                                                      # Obtained from Sensory
enrollmentType = none, jwt, or sharedSecret                                     # Selected by user
isSecure = True or False                                                        # Selected by user

[examples-configuration]
userId = my-user-name                                                           # Selected by user

[client-configuration]
clientid = my-client-id                                                         # Set by registration_examples.py
clientsecret = my-client-secret                                                 # Set by registration_examples.py
```

## Get Models
Depending on the contract with Sensory, you will have access to various audio and/or video models.  The AudioService and VideoService both have
methods that allow the user to see which models they have access to.  The `get_models_examples.py` file shows how both
the audio and video models that are available can be identified.

## Enrollment
Once your device has been registered you can start creating enrollments and enrollment groups by running the `enrollment_examples.py` script.  
There are three types of enrollments that will be covered.

- Audio Enrollments
- Audio Event Enrollments
- Video Enrollments

An enrollment group will then be created for each type of enrollment and there are example functions that show how to check the existing enrollments and enrollment groups. 
There are also example functions that retrieve existing enrollments and enrollment groups.  Those will probably be empty before you run the example code, but they will be populated with the enrollments and  enrollment groups you create by the end of the enrollment examples. The example enrollment code can be seen in the `enrollment_examples.py` file.
After running the enrollment examples, the `examples-configuration` section of the `config.ini` should be fully populated with enrollment ids and enrollment group ids like so:
```
[SDK-configuration]
fullyQualifiedDomainName = my.unique.domain.com                                 # Obtained from Sensory
tenantId = my-tenant-id                                                         # Obtained from Sensory
credential = my-credential                                                      # Obtained from Sensory
enrollmentType = none, jwt, or sharedSecret                                     # Selected by user
isSecure = True or False                                                        # Selected by user

[examples-configuration]
userId = my-user-name                                                           # Selected by user
audio_enrollment_id = my-audio-enrollment-id                                    # Set by enrollment_examples.py
audio_enrollment_group_id = my-audio-enrollment-group-id                        # Set by enrollment_examples.py
audio_event_enrollment_id = my-audio-event-enrollment-id                        # Set by enrollment_examples.py
audio_event_enrollment_group_id = my-audio-event-enrollment-group-id            # Set by enrollment_examples.py
video_enrollment_id = my-video-enrollment-id                                    # Set by enrollment_examples.py
video_enrollment_group_id = my-video-enrollment-group-id                        # Set by enrollment_examples.py

[client-configuration]
clientid = my-client-id                                                         # Set by registration_examples.py
clientsecret = my-client-secret                                                 # Set by registration_examples.py
```

NOTE: Other than the example_get_enrollments() and example_get_group_enrollments() functions, it is recommended that the functions defined in this file be run only once in the order 
they are defined in to avoid creating redundant enrollments.

## Authentication
Once the enrollment examples are complete, all of the fields in the `config.json` file should be populated and we can authenticate against the individual enrollments and
the enrollment groups.  There are examples that show how to authenticate against the following enrollments and enrollment groups

- Audio Authentication
- Audio Group Authentication
- Audio Enrolled Event Authentication
- Audio Enrolled Event Group Authentication
- Video Authentication
- Video Group Authentication

These examples are all shown in the `authentication_examples.py` file.

## Audio Events
Audio events operate function similarly to authentication in the sense that various sounds can be detected and identified.  Unlike authentication,
no enrollment is required to run the event detection models.  A sample implementation of one of Sensory's audio event models is shown in 
`audio_event_examples.py`.

## Audio Transcription
Similar to audio events, audio transcription models can be run without enrollment.  The `audio_transcription_examples.py`
file shows a sample implementation of one of Sensory's speech to text models.  The transcription models use a seven second sliding window that contain
the transcript of the most recent seven seconds.  There are two example functions in `audio_transcription_examples.py` for live audio - one that shows 
how to access the most recent seven second window of the transcription, and one that returns the transcript of the entire recording.

## Video Liveness
Video liveness models return a boolean denoting whether or not a live person is detected in a set of images or a video recording.  For example,
a picture of someone's face on a mobile device would not pass the liveness check.  A sample implementation is shown in the `video_liveness_examples.py`
file.  

## Health Service
It's important to check the health of your Sensory Inference server. You can do so by following the example in `health_service_examples.py`.

## Batch Audio Transcription
The `sensory_cloud_stt.py` file allows users to transcribe batches of wav files.  The script is setup to recieve a csv file with a column
of file paths to be transcribed called `audio_file` and an optional column of expected transcripts called `expected_transcript`.  If the expected
transcipts are present then the error rate is calculated for each individual file and for the entire corpus of files.  A yaml file containing
the stt configuration parameters is required as a command line argument to run the script.  The command line call will look like the statement below:

`python sensory_cloud_stt.py --config_path=/path/to/config.yaml`

### Sample Yaml Config File
```
stt-config:
  sensory_cloud_config_path: /path/to/sensory-cloud/config.ini
  model_name: speech_recognition_en
  audio_channel_count: 1
  sample_rate_hertz: 16000
  language_code: en-US
  enable_punctuation_capitalization: False
  do_single_utterance: False
  vad_sensitivity: 
  vad_duration: 
  custom_vocab_reward_threshold: 
  custom_vocabulary_id: 
  custom_word_list: 
  chunkmsec: 100 (chunk size in ms of audio that is passed up to sensory cloud)
  score_type: wer or cer (wer = word error rate, cer = character error rate)
  strip_spaces: False (set to True for cer)

io-config:
  input_path: /path/to/input-file.csv
  output_path: /path/to/output-file.csv
```

### Batch Audio Transcription Requirements
- pip install sensory-cloud
- pip install PyYAML
- pip install jiwer
- pip install Wave
- pip install pandas
