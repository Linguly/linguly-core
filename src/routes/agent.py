from fastapi import APIRouter
from typing import List
from src.agent_proxy.types import Agent, Message
from src.agent_proxy import agent_proxy
from fastapi import HTTPException, status, Body

router = APIRouter()

@router.get("/agents", response_model=List[Agent])
def read_agents():
    return agent_proxy.get_available_agents()

@router.post("/agent/{agent_id}/chat", response_model=Message)
def message_agent(agent_id: str, user_message: Message = Body(...)):
    if not user_message or not user_message.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message format"
        )
    try:
        return agent_proxy.message_agent(agent_id=agent_id, user_message=user_message)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
