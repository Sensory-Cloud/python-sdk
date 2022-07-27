"""
NOTE: Other than the example_get_enrollments() and example_get_group_enrollments() functions,
it is recommended that the functions defined in this file be run only once in the order 
they are defined to avoid creating redundant enrollments.
"""

import json
import uuid
import helpers

from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.services.video_service import VideoService
from sensory_cloud.services.management_service import ManagementService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2
import sensory_cloud.generated.v1.management.enrollment_pb2 as enrollment_pb2


def example_get_enrollments() -> enrollment_pb2.GetEnrollmentsResponse:
    """
    Example of retrieving all enrollments registered to the user_id set in
    the config.ini file.

    Returns:
        An enrollment_pb2.GetEnrollmentsResponse containing information about
        all enrollments
    """

    management_service: ManagementService = helpers.get_management_service()

    enrollments: enrollment_pb2.GetEnrollmentsResponse = (
        management_service.get_enrollments(
            user_id=helpers.environment_config.get("examples-configuration", "userId")
        )
    )

    return enrollments


def example_get_group_enrollments() -> enrollment_pb2.GetEnrollmentGroupsResponse:
    """
    Example of retrieving all enrollment groups registered to the user_id set in
    the config.ini file.

    Returns:
        An enrollment_pb2.GetEnrollmentGroupsResponse containing information about
        all enrollment groups
    """

    management_service: ManagementService = helpers.get_management_service()

    enrollment_groups: enrollment_pb2.GetEnrollmentGroupsResponse = (
        management_service.get_enrollment_groups(
            user_id=helpers.environment_config.get("examples-configuration", "userId")
        )
    )

    return enrollment_groups


def example_enroll_with_audio() -> str:
    """
    Example of creating a new audio enrollment with the Open Sesame
    wake word model.  This function will update the config.ini file with
    the newly generated enrollment id so long as the enrollment was successful.

    NOTE: This function should only be run once if the enrollment is successful.
    The enrollment id associated with the enrollment created will be written to
    the config.ini file so it can be easily accessed to authenticate against in
    the authentication examples.

    Returns:
        A string containing the the enrollment id if successful, otherwise None
    """

    enrollment_id: str = helpers.environment_config.get(
        "examples-configuration", "audio_enrollment_id", fallback=None
    )
    if enrollment_id is not None:
        print(f"Audio enrollment, {enrollment_id}, already exists")
        return

    model_name: str = "wakeword-16kHz-open_sesame.ubm"
    enrollment_description: str = "my open sesame wakeword enrollment"

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    enrollment_stream = audio_service.stream_enrollment(
        audio_config=audio_config,
        description=enrollment_description,
        user_id=helpers.environment_config.get("examples-configuration", "userId"),
        device_id=helpers.environment_config.get("SDK-configuration", "deviceId"),
        model_name=model_name,
        is_liveness_enabled=False,
        audio_stream_iterator=audio_stream_iterator,
    )

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

    if enrollment_id is not None:
        helpers.environment_config.set(
            "examples-configuration", "audio_enrollment_id", enrollment_id
        )

        with open(helpers.config_path, "w") as config_file:
            helpers.environment_config.write(config_file)

    return enrollment_id


def example_create_audio_enrollment_group() -> enrollment_pb2.EnrollmentGroupResponse:
    """
    Example creating an audio enrollment group that contains the audio enrollment that
    was generated in the example_enroll_with_audio() function.  All enrollments in an
    enrollment group must use the same model, so we are using the 'wakeword-16kHz-open_sesame.ubm'
    again.  The enrollment group name and description are set below in this function and the
    enrollment group_id is set by the user in the 'audio_enrollment_group_id' field of the config.ini
    file.

    Returns:
        An enrollment_pb2.EnrollmentGroupResponse for the new audio enrollment group created
    """

    group_id: str = helpers.environment_config.get(
        "examples-configuration", "audio_enrollment_group_id", fallback=None
    )
    if group_id is not None:
        print(f"Audio enrollment group, {group_id}, already exists")
        return

    enrollment_id: str = helpers.environment_config.get(
        "examples-configuration", "audio_enrollment_id", fallback=None
    )
    if enrollment_id is None:
        print(
            "An audio enrollment needs to be generated before an enrollment group can be created."
        )
        print(
            "Run the function, example_enroll_with_audio(), to generate an audio enrollment"
        )
        return

    model_name: str = "wakeword-16kHz-open_sesame.ubm"
    description: str = "my open sesame enrollment group"
    group_name: str = "my-audio-enrollment-group"

    management_service: ManagementService = helpers.get_management_service()

    group_id: str = str(uuid.uuid4())
    enrollment_group_response: enrollment_pb2.EnrollmentGroupResponse = (
        management_service.create_enrollment_group(
            user_id=helpers.environment_config.get("examples-configuration", "userId"),
            group_id=group_id,
            group_name=group_name,
            description=description,
            model_name=model_name,
            enrollment_ids=[enrollment_id],
        )
    )

    helpers.environment_config.set(
        "examples-configuration", "audio_enrollment_group_id", group_id
    )
    with open(helpers.config_path, "w") as config_file:
        helpers.environment_config.write(config_file)

    return enrollment_group_response


def example_create_enrolled_event() -> str:
    """
    Example of creating a new audio enrolled event.  This function will update
    the config.ini file with the newly generated enrollment id so long as the
    enrollment was successful.

    NOTE: This function should only be run once if the enrollment is successful.
    The enrollment id associated with the enrollment created will be written to
    the config.ini file so it can be easily accessed to authenticate against in
    the authentication examples.

    Returns:
        A string containing the the enrollment id if successful, otherwise None
    """

    enrollment_id: str = helpers.environment_config.get(
        "examples-configuration", "audio_event_enrollment_id", fallback=None
    )
    if enrollment_id is not None:
        print(f"Audio event enrollment, {enrollment_id}, already exists")
        return

    model_name: str = "sound-dependent-16kHz.ubm"
    description: str = "hey sensory enrolled event"

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    enrolled_event_stream = audio_service.stream_create_enrolled_event(
        audio_config=audio_config,
        description=description,
        user_id=helpers.environment_config.get("examples-configuration", "userId"),
        model_name=model_name,
        audio_stream_iterator=audio_stream_iterator,
    )

    try:
        print(
            "Recording enrollment (repeat saying 'Hey Sensory' or whatever enrollment phrase you choose until the enrollment is complete)..."
        )
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

    if enrollment_id is not None:
        helpers.environment_config.set(
            "examples-configuration", "audio_event_enrollment_id", enrollment_id
        )

        with open(helpers.config_path, "w") as config_file:
            helpers.environment_config.write(config_file)

    return enrollment_id


def example_create_audio_event_enrollment_group() -> enrollment_pb2.EnrollmentGroupResponse:
    """
    Example creating an audio event enrollment group that contains the audio enrollment that
    was generated in the example_create_enrolled_event() function.  All enrollments in an
    enrollment group must use the same model, so we are using the 'sound-dependent-16kHz.ubm'
    again.  The enrollment group name and description are set below in this function and the
    enrollment group_id is set by the user in the 'audio_event_enrollment_group_id' field of
    the config.ini file.

    Returns:
        An enrollment_pb2.EnrollmentGroupResponse for the new audio enrollment group created
    """

    group_id: str = helpers.environment_config.get(
        "examples-configuration", "audio_event_enrollment_group_id", fallback=None
    )
    if group_id is not None:
        print(f"Audio event enrollment group, {group_id}, already exists")
        return

    enrollment_id: str = helpers.environment_config.get(
        "examples-configuration", "audio_event_enrollment_id", fallback=None
    )
    if enrollment_id is None:
        print(
            "An audio event enrollment needs to be generated before an enrollment group can be created."
        )
        print(
            "Run the function, example_create_enrolled_event(), to generate an audio event enrollment"
        )
        return

    model_name: str = "sound-dependent-16kHz.ubm"
    group_name: str = "my-audio-event-enrollment-group"
    description: str = "my hey sensory enrollment group"

    management_service: ManagementService = helpers.get_management_service()

    group_id: str = str(uuid.uuid4())
    enrollment_group_response: enrollment_pb2.EnrollmentGroupResponse = (
        management_service.create_enrollment_group(
            user_id=helpers.environment_config.get("examples-configuration", "userId"),
            group_id=group_id,
            group_name=group_name,
            description=description,
            model_name=model_name,
            enrollment_ids=[enrollment_id],
        )
    )

    helpers.environment_config.set(
        "examples-configuration", "audio_event_enrollment_group_id", group_id
    )
    with open(helpers.config_path, "w") as config_file:
        helpers.environment_config.write(config_file)

    return enrollment_group_response


def example_enroll_with_video() -> str:
    """
    Example of creating a new video enrollment This function will update the
    config.ini file with the newly generated enrollment id so long as the
    enrollment was successful.

    NOTE: This function should only be run once if the enrollment is successful.
    The enrollment id associated with the enrollment created will be written to
    the config.ini file so it can be easily accessed to authenticate against in
    the authentication examples.

    Returns:
        A string containing the the enrollment id if successful, otherwise None
    """

    enrollment_id: str = helpers.environment_config.get(
        "examples-configuration", "video_enrollment_id", fallback=None
    )
    if enrollment_id is not None:
        print(f"Video event enrollment, {enrollment_id}, already exists")
        return

    model_name: str = "face_biometric_hektor"
    description: str = "my video enrollment"

    video_service: VideoService = helpers.get_video_service()

    video_stream_iterator: helpers.VideoStreamIterator = helpers.VideoStreamIterator()

    enrollment_stream = video_service.stream_enrollment(
        description=description,
        user_id=helpers.environment_config.get("examples-configuration", "userId"),
        device_id=helpers.environment_config.get("SDK-configuration", "deviceId"),
        model_name=model_name,
        is_liveness_enabled=False,
        video_stream_iterator=video_stream_iterator,
    )

    print("Recording enrollment, face your camera until complete...")
    percent_complete = 0
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

    if enrollment_id is not None:
        helpers.environment_config.set(
            "examples-configuration", "video_enrollment_id", enrollment_id
        )

        with open(helpers.config_path, "w") as config_file:
            helpers.environment_config.write(config_file)

    return enrollment_id


def example_create_video_enrollment_group() -> enrollment_pb2.EnrollmentGroupResponse:
    """
    Example creating a video event enrollment group that contains the video enrollment that
    was generated in the example_enroll_with_video() function.  All enrollments in an
    enrollment group must use the same model, so we are using the 'face_biometric_hektor'.
    The enrollment group name and description are set below in this function and the
    enrollment group_id is set by the user in the 'video_enrollment_group_id' field of
    the config.ini file.

    Returns:
        An enrollment_pb2.EnrollmentGroupResponse for the new audio enrollment group created
    """

    group_id: str = helpers.environment_config.get(
        "examples-configuration", "video_enrollment_group_id", fallback=None
    )
    if group_id is not None:
        print(f"Video event enrollment group, {group_id}, already exists")
        return

    enrollment_id: str = helpers.environment_config.get(
        "examples-configuration", "video_enrollment_id", fallback=None
    )
    if enrollment_id is None:
        print(
            "A video enrollment needs to be generated before an enrollment group can be created."
        )
        print(
            "Run the function, example_enroll_with_video(), to generate a video enrollment"
        )
        return

    model_name: str = "face_biometric_hektor"
    group_name: str = "my-video-enrollment-group"
    description: str = "my video enrollment group"

    management_service: ManagementService = helpers.get_management_service()

    group_id: str = str(uuid.uuid4())
    enrollment_group_response: enrollment_pb2.EnrollmentGroupResponse = (
        management_service.create_enrollment_group(
            user_id=helpers.environment_config.get("examples-configuration", "userId"),
            group_id=group_id,
            group_name=group_name,
            description=description,
            model_name=model_name,
            enrollment_ids=[enrollment_id],
        )
    )

    helpers.environment_config.set(
        "examples-configuration", "video_enrollment_group_id", group_id
    )
    with open(helpers.config_path, "w") as config_file:
        helpers.environment_config.write(config_file)

    return enrollment_group_response


if __name__ == "__main__":

    """
    The enrollment/create enrollment group function calls below are deliberately
    commented out because it is recommended that they are only run once.  Running
    these functions multiple times will create redundant enrollments and enrollment groups.
    It will also cause errors if the create enrollment group functions are called before
    the enrollment functions.  For example, the example_create_audio_enrollment_group()
    will put the enrollment created by example_enroll_with_audio() into an enrollment group,
    but that cannot happen if the audio enrollment does not exist.  It is recommended that
    the commented function calls be run just once (assuming they execute successfully) in
    the order they are shown, and then commented again upon completion.
    """

    # audio_enrollment_id: str = example_enroll_with_audio()
    # audio_enrollment_group_id: enrollment_pb2.EnrollmentGroupResponse = (
    #     example_create_audio_enrollment_group()
    # )

    # audio_event_enrollment_id: str = example_create_enrolled_event()
    # audio_event_enrollment_group_id: enrollment_pb2.EnrollmentGroupResponse = (
    #     example_create_audio_event_enrollment_group()
    # )

    # video_enrollment_id: str = example_enroll_with_video()
    # video_enrollment_group_response: enrollment_pb2.EnrollmentGroupResponse = (
    #     example_create_video_enrollment_group()
    # )

    # enrollment_group_response = example_create_video_enrollment_group()

    """
    The example_get_enrollments() and example_get_group_enrollments() can be called 
    as many times as you'd like and a good experiment is to run them before and after
    the creation of the enrollments/enrollment groups to confirm everything is working
    as expected.
    """

    enrollments: enrollment_pb2.GetEnrollmentsResponse = example_get_enrollments()
    enrollment_groups: enrollment_pb2.GetEnrollmentGroupsResponse = (
        example_get_group_enrollments()
    )
