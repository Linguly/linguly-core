from pydantic import BaseModel
from typing import List


class Agent(BaseModel):
    """
    Agent metadata to return based on available agents
    """

    id: str
    type: str
    display_name: str
    category: List[str]
    interaction_type: List[str]
    model_connector_id: str


class Message(BaseModel):
    role: str
    content: str
