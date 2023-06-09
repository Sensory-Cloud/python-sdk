import typing

import helpers

from sensory_cloud.services.assistant_service import AssistantService
import sensory_cloud.generated.v1.assistant.assistant_pb2 as assistant_pb2


def example_text_chat() -> assistant_pb2.TextChatResponse:
    """
    Function that illustrates an example of interfacing with the Sensory Cloud
    assistant through the python sdk

    Returns:
        A TextChatResponse object containing the assistant's response to the input
    """

    token_manager: helpers.TokenManager = helpers.get_token_manager()
    assistant_service: AssistantService = AssistantService(
        config=token_manager.oauth_service._config, token_manager=token_manager
    )
    message_content: typing.List[str] = ["What is a large language model?"]

    response: assistant_pb2.TextChatResponse = assistant_service.text_chat(
        message_content=message_content
    )

    return response


if __name__ == "__main__":
    response: assistant_pb2.TextChatResponse = example_text_chat()
