
from pydantic import BaseModel

# Agent metadata to return based on available agents
class Agent(BaseModel):
    id: str
    type: str
    display_name: str
    
class Message(BaseModel):
    content: str