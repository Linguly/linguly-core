from fastapi import APIRouter
from typing import List
from src.agent_proxy.types import Agent, Message
from src.agent_proxy import agent_proxy
from fastapi import HTTPException, status, Body

router = APIRouter()

@router.get("/agents", response_model=List[Agent])
def read_agents():
    return agent_proxy.get_available_agents()

@router.post("/agent", response_model=Message)
def message_agent(user_message: Message = Body(...)):
    if not user_message or not user_message.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message format"
        )
    return agent_proxy.message_agent(agent_id="1_dictionary", user_message=user_message)
