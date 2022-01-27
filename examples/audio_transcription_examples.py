import helpers

from sensory_cloud.services.audio_service import AudioService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


def example_audio_transcription() -> str:
    """
    Example of an audio transcription using the 'speech_recognition_en' speech
    to text model.  This function will record the transcription in a string and
    return the transcription string when the word 'exit' is spoken by the user.

    Returns:
        A string containing a complete transcription
    """

    transcription_model: str = "speech_recognition_en"

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    transcribe_stream = audio_service.stream_transcription(
        audio_config=audio_config,
        user_id=helpers.environment_config["user_id"],
        model_name=transcription_model,
        audio_stream_iterator=audio_stream_iterator,
    )

    transcription: str = None
    try:
        print("Transcription session begin (say exit to stop recording)...\n")
        for response in transcribe_stream:
            if "exit" in response.transcript:
                transcription = response.transcript.replace("exit", "")
                print(f"Transcription = {transcription}\n")
                break
        print("Transcription complete, ending session")
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        transcribe_stream.cancel()

    return transcription


if __name__ == "__main__":
    transcription = example_audio_transcription()
