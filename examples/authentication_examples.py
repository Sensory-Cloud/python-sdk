import helpers

from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.services.video_service import VideoService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


def example_authenticate_with_audio() -> bool:
    """
    Example of voice authentication against the Open Sesame wake word model
    created in enrollment_examples.py

    Returns:
        A boolean denoting whether or not the authentication was successful
    """

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    authenticate_stream = audio_service.stream_authenticate(
        audio_config=audio_config,
        enrollment_id=helpers.environment_config["audio_enrollment_id"],
        is_liveness_enabled=False,
        audio_stream_iterator=audio_stream_iterator,
    )

    authentication_success: bool = False
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
    from the enrollment group created in enrollment_examples.py

    Returns:
        A boolean denoting whether or not the authentication was successful
    """

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    authenticate_stream = audio_service.stream_group_authenticate(
        audio_config=audio_config,
        enrollment_group_id=helpers.environment_config["audio_enrollment_group_id"],
        is_liveness_enabled=False,
        audio_stream_iterator=audio_stream_iterator,
    )

    authentication_success: bool = False
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


def example_validate_enrolled_event() -> bool:
    """
    Example validating against the enrollment created in enrollment_examples.py

    Returns:
        A boolean denoting whether or not the validation was successful
    """

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    validate_enrolled_event_stream = audio_service.stream_validate_enrolled_event(
        audio_config=audio_config,
        enrollment_id=helpers.environment_config["audio_event_enrollment_id"],
        audio_stream_iterator=audio_stream_iterator,
    )

    authentication_success: bool = False
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


def example_group_validate_enrolled_event() -> bool:
    """
    Example validating against the enrollment group containing created in
    enrollment_examples.py

    Returns:
        A boolean denoting whether or not the validation was successful
    """

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    validate_enrolled_event_stream = audio_service.stream_group_validate_enrolled_event(
        audio_config=audio_config,
        enrollment_group_id=helpers.environment_config[
            "audio_event_enrollment_group_id"
        ],
        audio_stream_iterator=audio_stream_iterator,
    )

    authentication_success: bool = False
    try:
        print("Authenticating group enrolled event...")
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


def example_authenticate_with_video() -> bool:
    """
    Example of face authentication against the video enrollment
    created in enrollment_examples.py

    Returns:
        A boolean denoting whether or not the authentication was successful
    """

    video_service: VideoService = helpers.get_video_service()

    video_stream_iterator: helpers.VideoStreamIterator = helpers.VideoStreamIterator()

    authenticate_stream = video_service.stream_authentication(
        enrollment_id=helpers.environment_config["video_enrollment_id"],
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

    return success


def example_group_authenticate_with_video() -> bool:
    """
    Example of face authentication against the video enrollment
    created in enrollment_examples.py

    Returns:
        A boolean denoting whether or not the authentication was successful
    """

    video_service: VideoService = helpers.get_video_service()

    video_stream_iterator: helpers.VideoStreamIterator = helpers.VideoStreamIterator()

    authenticate_stream = video_service.stream_group_authentication(
        enrollment_group_id=helpers.environment_config["video_enrollment_group_id"],
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

    return success


if __name__ == "__main__":
    authenticate_with_audio = example_authenticate_with_audio()
    group_authenticate_with_audio = example_group_authenticate_with_audio()

    validate_enrolled_event = example_validate_enrolled_event()
    group_validate_enrolled_event = example_group_validate_enrolled_event()

    authenticate_with_video = example_authenticate_with_video()
    group_authenticate_with_video = example_group_authenticate_with_video()
