from pydantic import BaseModel
from bson import ObjectId


class Goal(BaseModel):
    id: str
    user_id: str
    language: str
    level: str  # e.g., "A1", "B2" (CEFR levels)
    context: str  # e.g., "general", "academic", "business"
    period: str  # e.g., "weeks", "months", "years"
    created_at: str  # ISO 8601 date string
    updated_at: str  # ISO 8601 date string

    def __init__(self, **data):
        if "_id" in data and isinstance(data["_id"], ObjectId):
            data["id"] = str(data["_id"])
        super().__init__(**data)


class GoalInput(BaseModel):
    language: str
    level: str  # e.g., "A1", "B2" (CEFR levels)
    context: str  # e.g., "general", "academic", "business"
    period: str  # e.g., "weeks", "months", "years"


class LearningPhrases(BaseModel):
    id: str
    user_id: str
    goal_id: str
    phrase: str
    used_count: int = 0  # Number of retrieves from agents
    tested_count: int = 0  # Number of test/feedback records
    success_count: int = 0  # Number of successes in tests/feedbacks
    success_record: list[bool] = (
        []
    )  # List of boolean values indicating success for each test/feedback record
    success_record_date: list[str] = []  # List of ISO 8601 date strings for each try
    last_used_date: str
    source_id: str  # e.g., "agent_id", "package_id"
    source_type: str  # e.g., "agent", "package"
