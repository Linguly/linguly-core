from src.model_proxy.types import ModelConnector, Message
from typing import List
import time


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
        print("Echo connector will echo the received message with a delay of 5 seconds")
        time.sleep(5)  # Add a 5 second delay to mimic real world scenario
        response = messages[0].content
        print("Echo connector response:", response)
        return Message(content=response, role="assistant")
