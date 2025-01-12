
from pydantic import BaseModel
from typing import List

class ModelConnector(BaseModel):
    """
    Agent metadata to return based on available agents
    """
    id: str
    type: str
    display_name: str
    model_name: str
    category: List[str]
    interaction_type: List[str]
    supported_languages: List[str]