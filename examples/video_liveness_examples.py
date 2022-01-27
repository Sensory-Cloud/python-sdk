import helpers

from sensory_cloud.services.video_service import VideoService


def example_stream_liveness_recognition() -> bool:
    """
    This function opens a video stream using the device camera and
    runs the stream through the liveness recognition model which detects
    the presence of a live person in frame.

    Returns:
        A boolean denoting whether or not a live person was detected in the
        video stream.
    """

    model_name: str = "face_recognition_mathilde"

    video_service: VideoService = helpers.get_video_service()

    video_stream_iterator: helpers.VideoStreamIterator = helpers.VideoStreamIterator()

    recognition_stream = video_service.stream_liveness_recognition(
        user_id=helpers.environment_config["user_id"],
        model_name=model_name,
        video_stream_iterator=video_stream_iterator,
    )

    alive: bool = False
    try:
        print("Running liveness recognition...")
        for response in recognition_stream:
            if response.isAlive:
                alive = True
                break
        print("You're alive!")
    except Exception as e:
        print(f"Liveness recognition failed with error {str(e)}")
    finally:
        video_stream_iterator.close()
        recognition_stream.cancel()

    return alive


if __name__ == "__main__":
    alive = example_stream_liveness_recognition()
