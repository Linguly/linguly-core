from src.shared_context.types import Goal, GoalInput
from typing import List
from src.db_proxy.db_proxy import get_db
from datetime import datetime
from bson import ObjectId


class Goals:
    """
    Goals class to manage user goals.
    """

    def __init__(self):
        self.db = get_db("shared_context")
        if not self.db:
            raise ValueError(
                "Database connection for shared_context not found. Please check your configuration."
            )

    def get_goals(self, user_id: str) -> List[Goal]:
        """
        Fetches the goals for a user based on their user ID.
        """
        goals = self.db.find("goals", {"user_id": user_id})
        if not goals:
            return []
        goals = [Goal(**goal) for goal in goals]
        return goals

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

    def select_goal(self, goal_id: str, user_id: str) -> bool:
        """
        Activates a goal for a user.
        """
        # Check if the goal exists
        try:
            goal_obj_id = ObjectId(goal_id)
        except Exception:
            raise ValueError(f"Invalid goal_id: {goal_id}")
        goals = self.db.find("goals", {"_id": goal_obj_id, "user_id": user_id})
        if not goals:
            print(f"Goal {goal_id} not found for user {user_id}.")
            raise ValueError(f"Goal {goal_id} not found for user {user_id}.")
        # Update the user's selected goal
        users = self.db.find("users", {"user_id": user_id}, limit=1)
        if not users:
            self.db.insert(
                "users",
                {
                    "user_id": user_id,
                    "selected_goal": goal_id,
                },
            )
            print(f"User {user_id} created with goal {goal_id}.")
        else:
            self.db.update(
                "users",
                {"user_id": user_id},
                {"$set": {"selected_goal": goal_id}},
            )
            print(f"User {user_id} updated with selected goal {goal_id}.")

    def get_selected_goal(self, user_id: str) -> Goal:
        """
        Fetches the currently selected goal for a user.
        """
        # Check if the user exists
        users = self.db.find("users", {"user_id": user_id}, limit=1)
        if not users:
            return None
        # Check if the user has a selected goal
        selected_goal_id = users[0].get("selected_goal")
        if not selected_goal_id:
            return None
        # Fetch the goal details
        goals = self.db.find("goals", {"_id": ObjectId(selected_goal_id)})
        if not goals:
            raise ValueError(
                f"Selected goal {selected_goal_id} not found for user {user_id}."
            )
        return Goal(**goals[0])
