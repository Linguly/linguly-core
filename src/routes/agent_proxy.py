from fastapi import APIRouter
from typing import List
from src.agent_proxy.types import Agent, Message

router = APIRouter()

@router.get("/agents", response_model=List[Agent])
def read_agents():
    return [{"id": "1", "type": "dictionary", "display_name": "dictionary_1"}]


@router.post("/agent", response_model=Message)
def message_agent():
    return [{"content": "Here is your first response from a Linguly Agent : )"}]
