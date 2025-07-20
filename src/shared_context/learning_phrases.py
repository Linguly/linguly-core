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
        user_id: str,
        goal_id: str,
        phrases: List[str],
        source_id: str,
        source_type: str,
    ):
        """
        add new learning phrases for a user.
        """
        now = datetime.utcnow().isoformat()
        for phrase in phrases:
            # Check if the phrase is not already recorded
            existing_phrase = self.db.find(
                "learning_phrases",
                {"user_id": user_id, "goal_id": goal_id, "phrase": phrase.lower()},
                limit=1,
            )
            if not existing_phrase:
                # Insert into the db
                phrase_id = self.db.insert(
                    "learning_phrases",
                    {
                        "user_id": user_id,
                        "goal_id": goal_id,
                        "phrase": phrase.lower(),
                        "used_count": 0,
                        "trial_count": 0,
                        "success_count": 0,
                        "trial_results": [],
                        "trial_dates": [],
                        "last_used_date": now,
                        "source_id": source_id,
                        "source_type": source_type,
                    },
                )

    def get_next_learning_phrases(
        self, user_id: str, goal_id: str, top: int
    ) -> List[str]:
        """
        Sort based on used_count asc and return top "top" number of phrases
        """
        phrases = self.db.find(
            "learning_phrases",
            {"user_id": user_id, "goal_id": goal_id},
            sort=[("used_count", 1)],
            limit=top,
        )
        # Update last_used_date and used_count for each phrase
        now = datetime.utcnow().isoformat()
        for phrase in phrases:
            self.db.update(
                "learning_phrases",
                {"_id": phrase["_id"]},
                {"$set": {"last_used_date": now}, "$inc": {"used_count": 1}},
            )
        # return the phrases only
        return [phrase["phrase"] for phrase in phrases]

    def update_learning_status(
        self, user_id: str, goal_id: str, phrase: str, success: bool
    ):
        """
        Based on the success status add a new record to the phrase test(trial) records
        """
        now = datetime.utcnow().isoformat()
        phrase_record = self.db.find(
            "learning_phrases",
            {"user_id": user_id, "goal_id": goal_id, "phrase": phrase.lower()},
            limit=1,
        )
        if not phrase_record:
            return
        # Update the phrase record using MongoDB based update operators
        update_data = {
            "$push": {"trial_dates": now, "trial_results": success},
            "$inc": {"trial_count": 1, "success_count": 1 if success else 0},
        }
        self.db.update(
            "learning_phrases",
            {"user_id": user_id, "goal_id": goal_id, "phrase": phrase.lower()},
            update_data,
        )
