import helpers

import wave
import threading
from queue import Queue

from sensory_cloud.services.audio_service import AudioService, TranscriptAggregator

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


class FileTranscriptionIterator:
    transcript = None
    responses = []
    _queue = Queue()
    _stop_event = threading.Event()

    def __init__(self):
        self._stop_event.set()

    def __iter__(self):
        return self

    def __next__(self):
        if self._stop_event.is_set():
            post_processing_action = None
            item = self._queue.get()
            self._queue.task_done()
            if item == "stop":
                post_processing_action = audio_pb2.AudioRequestPostProcessingAction(
                    action=audio_pb2.AudioPostProcessingAction.FINAL
                )
                item = b""
                self.stop()
            _next = (item, post_processing_action)
            return _next
        raise StopIteration

    def put(self, item):
        self._queue.put(item)

    def stop(self):
        self._stop_event.clear()


def example_wave_file_transcription(file_path: str) -> str:
    """
    Example of an audio transcription using the 'speech_recognition_en' speech
    to text model.  This function will read in a wave file and return the
    transcription as a string.

    Args:
        file_path: path to wave file to be transcribed

    Returns:
        A string containing a complete transcription
    """

    frames_per_buffer: int = 1024

    transcription_iterator: FileTranscriptionIterator = FileTranscriptionIterator()

    with wave.open(file_path, "rb") as wave_file:
        buffer: bytes = wave_file.readframes(frames_per_buffer)
        while buffer != b"":
            transcription_iterator.put(buffer)
            buffer: bytes = wave_file.readframes(frames_per_buffer)

    transcription_iterator.put("stop")

    transcription_model: str = "speech_recognition_en"

    audio_service: AudioService = helpers.get_audio_service()
    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()

    transcribe_stream = audio_service.stream_transcription(
        audio_config=audio_config,
        user_id=helpers.environment_config.get("examples-configuration", "userId"),
        model_name=transcription_model,
        enable_punctuation_capitalization=True,
        audio_stream_iterator=transcription_iterator,
        do_offline_mode=True,
    )

    transcript_aggregator: TranscriptAggregator = TranscriptAggregator()

    try:
        print("Transcription session begin ...")
        for response in transcribe_stream:
            transcript_aggregator.process_response(response)
            full_transcript = transcript_aggregator.get_transcript()
            transcription_iterator.transcript = full_transcript
            transcription_iterator.responses.append(response)
        print("Transcription complete, ending session")
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}")
    finally:
        transcribe_stream.cancel()

    transcript: str = transcript_aggregator.get_transcript()

    return transcript
