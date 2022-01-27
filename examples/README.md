# Sensory Cloud Python SDK Examples

## Python Environment
The Sensory Cloud python SDK is supported for python >= 3.6.  Before running the examples described below, the following packages must be
installed:

```
pip install sensory-cloud
pip install PyAudio
pip install opencv-python
pip install Pillow
```

## Setting Up Configuration Parameters
Before starting with these examples you will need to create json config file called `config.json`  in this directory as shown below.

```
{
    "fully_qualified_domain_name": "my.unique.domain.com",                      # Obtained from Sensory
    "tenant_id": "my-tenant-id",                                                # Obtained from Sensory
    "tenant_secret": "my-tenant-secret",                                        # Obtained from Sensory

    "device_id": "my-device-id",                                                # Selected by user
    "device_name": "my-device-name",                                            # Selected by user
    "user_id": "my-user-id",                                                    # Selected by user
    "audio_enrollment_group_id": "my-audio-enrollment-group-id",                # Selected by user
    "audio_event_enrollment_group_id": "my-audio-event-enrollment-group-id",    # Selected by user
    "video_enrollment_group_id": "my-video-enrollment-group-id",                # Selected by user

    "client_id": "",                                                            # Set in registration_examples.py
    "client_secret": "",                                                        # Set in registration_examples.py

    "audio_enrollment_id": "",                                                  # Set in enrollment_examples.py
    "audio_event_enrollment_id": "",                                            # Set in enrollment_examples.py
    "video_enrollment_id": ""                                                   # Set in enrollment_examples.py
}
```

The `fully_qualified_domain_name`, `tenant_id`, and `tenant_secret` are obtained from Sensory upon registration and those credentials should
be placed in the `config.json` file.  The `device_id`, `device_name`, `user_id`, `audio_enrollment_group_id`, `audio_event_enrollment_group_id`, 
and `video_enrollment_group_id` can be chosen by the user and added to the config file as well.  The remaining configuration parameters 
will be set as we work through the registration and enrollment examples.

## Helpers
The [helpers.py](helpers.py) file has several helper functions that are used throughout the examples discussed below.  For example,
the `helpers.py` defines the AudioStreamIterator class which interfaces with your device microphone and the VideoStreamIterator class that
interfaces with your device camera.  There are also helper functions that create instances of the AudioService, VideoService, and ManagementService
which are used frequently.

## Registration
The first step in using the Sensory Cloud Python SDK is to setup client credentials and register your device.  An example of this process is covered
in [registration_examples.py](registration_examples.py).  After running the registration examples, the `client_id` and `client_secret` fields in
the `config.json` file should be populated.

## Get Models
Depending on the contract with Sensory, you will have access to various audio and/or video models.  The AudioService and VideoService both have
methods that allow the user to see which models they have access to.  The [get_models_examples.py](get_models_examples.py) file shows how both
the audio and video models that are available can be identified.

## Enrollment
Once your device has been registered you can start creating enrollments and enrollment groups.  There are three types of enrollments that will be 
covered.

- Audio Enrollments
- Audio Event Enrollments
- Video Enrollments

An enrollment group will then be created for each type of enrollment and there are example functions that show how to check the existing enrollments and enrollment groups. 
The `audio_enrollment_group_id`, `audio_event_enrollment_group_id`, and the `video_enrollment_group_id` fields in the `config.json` file will be used for creating their
corresponding enrollment groups, so make sure those fields are populated before running any of the create enrollment group example functions.  There are also example functions
that retrieve existing enrollments and enrollment groups.  Those will probably be empty before you run the example code, but they will be populated with the enrollments and 
enrollment groups you create by the end of the enrollment examples. The example enrollment code can be seen in the [enrollment_examples.py](enrollment_examples.py) file.
After running the enrollment examples, the `audio_enrollment_id`, `audio_event_enrollment_id`, and the `video_enrollment_id` fields in the `config.json` file should be populated.

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

These examples are all shown in the [authentication_examples.py](authentication_examples.py) file.

## Audio Events
Audio events operate function similarly to authentication in the sense that various sounds can be detected and identified.  Unlike authentication,
no enrollment is required to run the event detection models.  A sample implementation of one of Sensory's audio event models is shown in 
[audio_event_examples.py](audio_event_examples.py).

## Audio Transcription
Similar to audio events, audio transcription models can be run without enrollment.  The [audio_transcription_examples.py](audio_transcription_examples.py)
file shows a sample implementation of one of Sensory's speech to text models.

## Video Liveness
Video liveness models return a boolean denoting whether or not a live person is detected in a set of images or a video recording.  For example,
a picture of someone's face on a mobile device would not pass the liveness check.  A sample implementation is shown in the [video_liveness_examples.py](video_liveness_examples.py)
file.  