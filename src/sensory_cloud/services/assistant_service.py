import typing
from enum import Enum

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, Metadata

import sensory_cloud.generated.v1.assistant.assistant_pb2 as assistant_pb2
import sensory_cloud.generated.v1.assistant.assistant_pb2_grpc as assistant_pb2_grpc


class RequestIterator:
    """
    The RequestIterator class facilitates the request streams that are sent to the
    grpc server.  There are six possible audio request types and and five request configurations
    that are given by the AudioRequest and RequestConfig enums respectively.  The first
    request sent must be a configuration request and all subsequent requests contain the audio
    content being streamed and any post processing actions if relevant.
    """

    _first_request: bool = True

    def __init__(
        self,
        request_config: assistant_pb2.AssistantMessageConfig,
        assistant_stream_iterator: typing.Iterable[typing.Union[bytes, str]],
    ):
        """
        Constructor method for the RequestIterator class

        Arguments:
            audio_request: AudioRequest enum denoting which type of request is being sent
            request_config: RequestConfig enum containing the initial request configuration
            audio_stream_iterator: Iterator containing audio bytes
        """

        self._request_config = request_config
        self._assistant_stream_iterator = assistant_stream_iterator

    def __iter__(self):
        return self

    def __next__(self) -> assistant_pb2.AssistantMessageRequest:
        if self._first_request:
            self._first_request = False
            return assistant_pb2.AssistantMessageRequest(config=self._request_config)
        else:
            return assistant_pb2.AssistantMessageRequest(
                message=next(self._assistant_stream_iterator)
            )


class AssistantService:
    """
    Class that handles communication with the sensory cloud assistant service
    """

    def __init__(self, config: Config, token_manager: ITokenManager):
        self._config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._assistant_service_client: assistant_pb2_grpc.AssistantServiceStub = (
            assistant_pb2_grpc.AssistantServiceStub(config.channel)
        )

    def process_message(
        self,
        user_id: str,
        device_id: str,
        model_name: str,
        include_audio_response: bool,
        message_iterator: typing.Iterable[assistant_pb2.AssistantMessage],
    ) -> typing.Iterable[assistant_pb2.AssistantMessageResponse]:
        """
        Method that sends messages to the sensory cloud assistant to be processed

        Arguments:
            user_id: String containing the user id
            device_id: String containing the device id
            model_name: String containing the model name
            include_audio_response: Boolean indicating whether or not audio should be included in the response
            message_iterator: Iterator of AssistantMessage objects

        Returns:
            An iterator of AssistantMessageResponse objects
        """

        config: assistant_pb2.AssistantMessageConfig = (
            assistant_pb2.AssistantMessageConfig(
                userId=user_id,
                deviceId=device_id,
                modelName=model_name,
                includeAudioResponse=include_audio_response,
            )
        )

        request_iterator: RequestIterator = RequestIterator(
            request_config=config, assistant_stream_iterator=message_iterator
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        assistant_stream: typing.Iterable[
            assistant_pb2.AssistantMessageResponse
        ] = self._assistant_service_client.ProcessMessage(
            request_iterator=request_iterator, metadata=metadata
        )

        return assistant_stream
