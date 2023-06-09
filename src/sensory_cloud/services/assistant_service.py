import typing

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, Metadata

import sensory_cloud.generated.v1.assistant.assistant_pb2 as assistant_pb2
import sensory_cloud.generated.v1.assistant.assistant_pb2_grpc as assistant_pb2_grpc


class AssistantService:
    """
    Class that handles all assistant requests to Sensory Cloud
    """

    def __init__(self, config: Config, token_manager: ITokenManager):
        """
        Constructor method for the AssistantService class

        Arguments:
            config: Config object containing the relevant grpc connection information
            token_manager: ITokenManager object that generates and returns JWT metadata
        """

        self._config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._client = assistant_pb2_grpc.AssistantServiceStub(config.channel)

    def text_chat(
        self,
        message_content: typing.List[str],
        model_name: str = "gpt-3.5-turbo",
        chat_role: assistant_pb2.ChatRole = assistant_pb2.ChatRole.USER,
    ) -> assistant_pb2.TextChatResponse:
        """
        Method that chats with Sensory Cloud's assistant

        Arguments:
            model_name: String containing the name of the chat model to be used
            message_content: A list of strings containing the content of the message
                to be sent to the chat model
            chat_role: ChatRole.SYSTEM, ChatRole.USER, or ChatRole.ASSISTANT

        Returns:
            A TextChatResponse object containing the assistant's response to the input
        """

        messages: typing.List[assistant_pb2.ChatMessage] = [
            assistant_pb2.ChatMessage(role=chat_role, content=message)
            for message in message_content
        ]

        request: assistant_pb2.TextChatRequest = assistant_pb2.TextChatRequest(
            modelName=model_name, messages=messages
        )
        metadata: Metadata = self._token_manager.get_authorization_metadata()

        response: assistant_pb2.TextChatResponse = self._client.TextChat(
            request=request, metadata=metadata
        )

        return response
