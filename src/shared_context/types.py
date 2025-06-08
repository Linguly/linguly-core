from pydantic import BaseModel


class Goal(BaseModel):
    _id: str
    user_id: str
    language: str
    level: str  # e.g., "A1", "B2" (CEFR levels)
    context: str  # e.g., "general", "academic", "business"
    period: str  # e.g., "weeks", "months", "years"
    created_at: str  # ISO 8601 date string
    updated_at: str  # ISO 8601 date string


class GoalInput(BaseModel):
    language: str
    level: str  # e.g., "A1", "B2" (CEFR levels)
    context: str  # e.g., "general", "academic", "business"
    period: str  # e.g., "weeks", "months", "years"


class LearningPhrases(BaseModel):
    _id: str
    user_id: str
    goal_id: str
    phrase: str
    used_count: int = 0
    success_count: int = 0
    source: str  # e.g., "agent_id", "package_id"
    source_type: str  # e.g., "agent", "package"
