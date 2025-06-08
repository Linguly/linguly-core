from src.shared_context.types import Goal, GoalInput
from typing import List
from src.db_proxy.db_proxy import get_db
from datetime import datetime


class Goals:
    """
    Goals class to manage user goals.
    """

    def __init__(self):
        self.db = get_db("shared_context")
        if not self.db:
            raise ValueError(
                "Database connection not found. Please check your configuration."
            )

    def get_goals(self, user_id: str) -> List[Goal]:
        """
        Fetches the goals for a user based on their user ID.
        """
        goals = self.db.find("goals", {"user_id": user_id})
        if not goals:
            return []
        return goals

    # create_goal(goal, current_user.user_id):
    def create_goal(self, goal: GoalInput, user_id: str) -> Goal:
        """
        Creates a new goal for a user.
        """
        now = datetime.utcnow().isoformat()
        goal_id = self.db.insert(
            "goals",
            {
                "user_id": user_id,
                "language": goal.language,
                "level": goal.level,
                "context": goal.context,
                "period": goal.period,
                "created_at": now,
                "updated_at": now,
            },
        )
        return True

    def select_goal(self, goal_id: str, user_id: str) -> bool:
        """
        Activates a goal for a user.
        This function is a placeholder and should be replaced with actual logic to activate a goal.
        """
        # Placeholder implementation
        # In a real application, you would update the goal's status in the database
        print(f"Goal {goal_id} activated for user {user_id}.")
        return True
