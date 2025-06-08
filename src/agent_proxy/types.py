from pydantic import BaseModel
from typing import List


class Agent(BaseModel):
    """
    Agent metadata to return based on available agents
    """

    id: str  # Unique per instance
    type: (
        str  # Unique per Agent Class, e.g. 'dictionary', 'masking', 'simple_chat', etc.
    )
    display_name: str  # Unique per instance
    category: List[str]  # Can be: tool, test, learning
    interaction_type: List[str]  # Can be: chat, voice, card
    model_connector_id: str  # Connector ID used to connect to the model, e.g. 'openai_1', 'ollama_2', etc.


class Message(BaseModel):
    role: str = "user"  # Default role is 'user'
    content: str
