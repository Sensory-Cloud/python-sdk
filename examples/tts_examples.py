import typing

import helpers

from sensory_cloud.services.audio_service import AudioService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


def example_text_to_speech(wav_path: str):
    """
    Example of text to speech synthesis using the us english male voice model
    that synthesises the phrase defined below and writes a wave file to the
    wav_path defined below as well
    """

    phrase: str = "testing one two three"
    voice_name: str = "craig"

    audio_config: audio_pb2.AudioConfig = helpers.get_audio_config()
    audio_config.sampleRateHertz = 22050

    audio_service: AudioService = helpers.get_audio_service()

    synthesis_stream: typing.Iterable[
        audio_pb2.SynthesizeSpeechResponse
    ] = audio_service.synthesize_speech(
        audio_config=audio_config, phrase=phrase, voice_name=voice_name
    )

    audio_bytes: bytes = b"".join([item.audioContent for item in synthesis_stream])

    with open(wav_path, "wb") as wave_file:
        wave_file.write(audio_bytes)


if __name__ == "__main__":
    """
    NOTE:
        This script will write a wav file called test_wav.wav in this directory
        unless the `wav_path` variable below is changed
    """
    wav_path = "wav_path.wav"

    example_text_to_speech(wav_path=wav_path)
