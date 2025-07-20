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
    try:
        goals.create_goal(goal, current_user.user_id)
        # Return a success message and status 201
        return {"message": "Goal created successfully."}, status.HTTP_201_CREATED
    except Exception as e:
        print(f"Error creating goal: {e}")
        # Raise an HTTP exception with status 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal creation failed. Please check the provided data.",
        )


@router.post("/goals/{goal_id}/select")
def select_goal(goal_id: str, current_user: UserInfo = Depends(get_current_user)):
    """Activate the selected goal for the current user."""
    try:
        goals.select_goal(goal_id, current_user.user_id)
        # Return a success message and status 201
        return {
            "message": "The selected goal activated successfully."
        }, status.HTTP_201_CREATED
    except Exception as e:
        print(f"Error selecting goal: {e}")
        # Raise an HTTP exception with status 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal selection failed. Please check the provided data.",
        )


# get the selected goal for the current user
@router.get("/goals/selected")
def get_selected_goal(current_user: UserInfo = Depends(get_current_user)):
    """Get the selected goal for the current user."""
    try:
        selected_goal = goals.get_selected_goal(current_user.user_id)
    except Exception as e:
        print(f"Error retrieving selected goal: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the selected goal.",
        )
    if not selected_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No selected goal found for the current user.",
        )
    return selected_goal
