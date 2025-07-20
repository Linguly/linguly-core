from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    role: str = "user"  # Default role is 'user'
    content: str


class Agent(BaseModel):
    """
    Agent metadata to return based on available agents
    """

    id: str  # Unique per instance
    type: (
        str  # Unique per Agent Class, e.g. 'dictionary', 'masking', 'simple_chat', etc.
    )
    display_name: str  # Unique per instance
    categories: List[str]  # Can be: utility, test, learning
    subcategories: List[str]  # Can be: add_to_learning_phrases, monitor_progress, etc.
    description: (
        str  # Description of the agent, shown in the UI when the agent is selected
    )
    interaction_types: List[str]  # Can be: chat, voice, card
    model_connector_id: str  # Connector ID used to connect to the model, e.g. 'openai_1', 'ollama_2', etc.
    compatible_interfaces: List[str]  # Can be: telegram, web, etc.
    supported_languages: List[
        str
    ]  # list of supported languages based on the connected model

    def start(user_id: str, goal_id: str) -> List[Message]:
        pass

    def reply(user_id: str, goal_id: str, messages: List[Message]) -> List[Message]:
        pass
