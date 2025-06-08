from fastapi import APIRouter, HTTPException, status, Depends
from src.user.user_auth import get_current_user
from src.user.types import UserInfo
from src.shared_context.goals import Goals
from src.shared_context.types import Goal, GoalInput

router = APIRouter()
goals = Goals()


@router.get("/goals", response_model=list[Goal])
def get_goals(current_user: UserInfo = Depends(get_current_user)):
    return goals.get_goals(current_user.user_id)


@router.post("/goals")
def create_goal(goal: GoalInput, current_user: UserInfo = Depends(get_current_user)):
    """Create a new goal for the current user."""
    if not goals.create_goal(goal, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal creation failed. Please check the provided data.",
        )
    # Return a success message and status 201
    return {"message": "Goal created successfully."}, status.HTTP_201_CREATED


@router.post("/goals/{goal_id}/select")
def select_goal(goal_id: str, current_user: UserInfo = Depends(get_current_user)):
    """Activate the selected goal for the current user."""
    if not goals.select_goal(goal_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found or not owned by the user.",
        )
    # Return a success message and status 201
    return {
        "message": "The selected goal activated successfully."
    }, status.HTTP_201_CREATED
