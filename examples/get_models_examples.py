import helpers

from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.services.video_service import VideoService

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2
import sensory_cloud.generated.v1.video.video_pb2 as video_pb2


def get_audio_models_example() -> audio_pb2.GetModelsResponse:
    """
    Example showing how the user can view all available audio models

    Returns:
        An audio_pb2.GetModelsResponse containing information about the
        audio models that are available
    """

    audio_service: AudioService = helpers.get_audio_service()

    audio_models: audio_pb2.GetModelsResponse = audio_service.get_models()

    return audio_models


def get_video_models_example() -> video_pb2.GetModelsResponse:
    """
    Example showing how the user can view all available video models

    Returns:
        A video_pb2.GetModelsResponse containing information about the
        video models that are available
    """

    video_service: VideoService = helpers.get_video_service()

    video_models: video_pb2.GetModelsResponse = video_service.get_models()

    return video_models


if __name__ == "__main__":
    audio_models = get_audio_models_example()
    video_models = get_video_models_example()
