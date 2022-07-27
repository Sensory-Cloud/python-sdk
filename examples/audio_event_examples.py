import helpers

from sensory_cloud.services.audio_service import AudioService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


def example_stream_event() -> str:
    """
    Example of an audio event detected by the 'sound-16kHz-combined-all.trg' model.
    This model detects sounds like coughing and door knocks, and this function  will
    exit once an event is detected.  A good way to trigger the door knock detection
    is to knock on a desk or table.

    Returns:
        A string containing the type of event detected
    """

    event_model: str = "sound-16kHz-combined-all.trg"

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    event_stream = audio_service.stream_event(
        audio_config=audio_config,
        user_id=helpers.environment_config.get("examples-configuration", "userId"),
        model_name=event_model,
        audio_stream_iterator=audio_stream_iterator,
    )

    event = None
    try:
        print("Listening for events...")
        for response in event_stream:
            if response.success:
                event = response.resultId
                break
        print(f"Detected {event}, ending session")
    except Exception as e:
        print(f"Event detection failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        event_stream.cancel()

    return event


if __name__ == "__main__":
    event = example_stream_event()
