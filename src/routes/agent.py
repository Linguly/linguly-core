from fastapi import APIRouter
from typing import List
from src.agent_proxy.types import Agent, Message
from src.agent_proxy import agent_proxy

router = APIRouter()

@router.get("/agents", response_model=List[Agent])
def read_agents():
    return agent_proxy.get_available_agents()


@router.post("/agent", response_model=Message)
def message_agent():
    return agent_proxy.message_agent(agent_id="1_dictionary", user_message = {"content": "test"} )
