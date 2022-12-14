import datetime
import wave
import typing
import threading
from queue import Queue

import helpers

from sensory_cloud.services.audio_service import AudioService, TranscriptAggregator

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


def example_audio_transcription_partial() -> str:
    """
    Example of an audio transcription using the 'speech_recognition_en' speech
    to text model.  This function will record ten seconds of audio and return
    the transcript for the final seven second sliding window.

    Returns:
        A string containing a partial transcription
    """

    transcription_model: str = "speech_recognition_en"

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_stream_iterator: helpers.AudioStreamIterator = (
        helpers.get_audio_stream_iterator(audio_config=audio_config)
    )

    transcribe_stream = audio_service.stream_transcription(
        audio_config=audio_config,
        user_id=helpers.environment_config.get("examples-configuration", "userId"),
        model_name=transcription_model,
        enable_punctuation_capitalization=True,
        audio_stream_iterator=audio_stream_iterator,
    )

    stop_time: datetime.datetime = datetime.datetime.now() + datetime.timedelta(
        seconds=10
    )
    try:
        print("Partial transcription session begin ...\n")
        for response in transcribe_stream:
            if datetime.datetime.now() > stop_time:
                break
        print("Transcription complete, ending session")
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        transcribe_stream.cancel()

    return response.transcript.strip()


def example_audio_transcription_full() -> str:
    """
    Example of an audio transcription using the 'speech_recognition_en' speech
    to text model.  This function will record ten seconds of audio and return
    the full transcription.

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
        user_id=helpers.environment_config.get("examples-configuration", "userId"),
        model_name=transcription_model,
        enable_punctuation_capitalization=True,
        audio_stream_iterator=audio_stream_iterator,
    )

    transcript_aggregator: TranscriptAggregator = TranscriptAggregator()

    stop_time: datetime.datetime = datetime.datetime.now() + datetime.timedelta(
        seconds=10
    )
    try:
        print("Full transcription session begin ...\n")
        for response in transcribe_stream:
            transcript_aggregator.process_response(response)
            if datetime.datetime.now() > stop_time:
                break
        print("Transcription complete, ending session")
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}\n")
    finally:
        audio_stream_iterator.close()
        transcribe_stream.cancel()

    transcript: str = transcript_aggregator.get_transcript()

    return transcript


if __name__ == "__main__":
    partial_transcript: str = example_audio_transcription_partial()
    full_transcript: str = example_audio_transcription_full()
