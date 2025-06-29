from src.model_proxy.types import ModelConnector, Message
from typing import List


class Echo(ModelConnector):
    """
    This Connector is a dummy connector to echo the user message for test scenarios
    """

    type: str = "test"  # Setting default value to the Connector's properties
    category: List[str] = ["language_model"]
    interaction_type: List[str] = ["text"]

    def __init__(self, **data):
        # Call the parent class constructor with the modified data
        super().__init__(**data)

    def reply(self, messages: List[Message]) -> Message:
        response = messages[0].content
        return Message(content=response, role="assistant")
