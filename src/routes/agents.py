from fastapi import APIRouter, HTTPException, status, Body, Depends, Query
from typing import List, Optional
from src.user.user_auth import validate_token, get_current_user
from src.user.types import UserInfo
from src.agent_proxy.types import Agent, Message
from src.agent_proxy import agent_proxy

router = APIRouter()


@router.get(
    "/agents", response_model=List[Agent], dependencies=[Depends(validate_token)]
)
def read_agents():
    return agent_proxy.get_available_agents()


@router.get(
    "/agents/filter",
    response_model=List[Agent],
    dependencies=[Depends(validate_token)],
)
def filter_agents(
    categories: Optional[List[str]] = Query(
        None, description="Filter by categories"
    ),
    subcategories: Optional[List[str]] = Query(
        None, description="Filter by subcategories"
    ),
    compatible_interfaces: Optional[List[str]] = Query(
        None, description="Filter by compatible interfaces"
    ),
):
    agents = agent_proxy.get_available_agents()
    if categories:
        agents = [
            a
            for a in agents
            if hasattr(a, "categories")
            and set(categories).issubset(set(a.categories))
        ]
    if subcategories:
        agents = [
            a
            for a in agents
            if hasattr(a, "subcategories")
            and set(subcategories).issubset(set(a.subcategories))
        ]
    if compatible_interfaces:
        agents = [
            a
            for a in agents
            if hasattr(a, "compatible_interfaces")
            and set(compatible_interfaces).issubset(set(a.compatible_interfaces))
        ]
    return agents


@router.post("/agents/{agent_id}/chat", response_model=Message)
def message_agent(
    agent_id: str,
    current_user: UserInfo = Depends(get_current_user),
    user_message: Message = Body(...),
):
    if not user_message or not user_message.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format"
        )
    try:
        return agent_proxy.message_agent(agent_id=agent_id, user_message=user_message)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
