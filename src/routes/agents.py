from fastapi import APIRouter, HTTPException, status, Body, Depends, Query
from typing import List, Optional
from src.user.user_auth import validate_token, get_current_user
from src.user.types import UserInfo
from src.agent_proxy.types import Agent, Message
from src.agent_proxy import agent_proxy

router = APIRouter()


@router.get(
    "/agents",
    response_model=List[Agent],
)
def read_agents(current_user: UserInfo = Depends(get_current_user)):
    return agent_proxy.get_available_agents(user_id=current_user.user_id)


@router.get(
    "/agents/filter",
    response_model=List[Agent],
)
def filter_agents(
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    subcategories: Optional[List[str]] = Query(
        None, description="Filter by subcategories"
    ),
    compatible_interfaces: Optional[List[str]] = Query(
        None, description="Filter by compatible interfaces"
    ),
    current_user: UserInfo = Depends(get_current_user),
):
    agents = agent_proxy.get_available_agents(user_id=current_user.user_id)
    if categories:
        agents = [
            a
            for a in agents
            if hasattr(a, "categories") and set(categories).issubset(set(a.categories))
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


@router.post("/agents/{agent_id}/start", response_model=List[Message])
def start_the_agent(
    agent_id: str,
    current_user: UserInfo = Depends(get_current_user),
):
    try:
        return agent_proxy.start_the_agent(
            agent_id=agent_id, user_id=current_user.user_id
        )
    except ValueError as e:
        print(f"Error starting the agent: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/agents/{agent_id}/chat", response_model=List[Message])
def chat_with_agent(
    agent_id: str,
    current_user: UserInfo = Depends(get_current_user),
    messages: List[Message] = Body(...),
):
    if not messages or not messages[0].content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format"
        )
    try:
        return agent_proxy.chat_with_agent(
            agent_id=agent_id, user_id=current_user.user_id, messages=messages
        )
    except ValueError as e:
        print(f"Error messaging agent: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
