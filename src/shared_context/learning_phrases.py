from typing import List
from src.db_proxy.db_proxy import get_db
from datetime import datetime


class LearningPhrases:
    """
    LearningPhrases class to manage Learning Phrases.
    """

    def __init__(self):
        self.db = get_db("shared_context")
        if not self.db:
            raise ValueError(
                "Database connection for shared_context not found. Please check your configuration."
            )

    def add_to_learning_phrases(
        self,
        phrases: List[str],
        user_id: str,
        goal_id: str,
        source_id: str,
        source_type: str,
    ):
        """
        add new learning phrases for a user.
        """
        now = datetime.utcnow().isoformat()
        for phrase in phrases:
            phrase_id = self.db.insert(
                "learning_phrases",
                {
                    "user_id": user_id,
                    "goal_id": goal_id,
                    "phrase": phrase,
                    "used_count": 0,
                    "tested_count": 0,
                    "success_count": 0,
                    "success_record": [],
                    "success_record_date": [],
                    "last_used_date": now,
                    "source_id": source_id,
                    "source_type": source_type,
                },
            )
