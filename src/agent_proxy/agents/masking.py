from src.agent_proxy.types import Agent, Message
from src.model_proxy import model_proxy
from src.db_proxy.db_proxy import get_db
from src.shared_context.types import Goal
from src.shared_context.learning_phrases import LearningPhrases
from pydantic import BaseModel
from typing import List, ClassVar
import asyncio
import re
import time

learning_phrases = LearningPhrases()
BLANK_MASK = "`______`"


class Configuration(BaseModel):
    """
    Agent Configuration. Unique per instance.
    """

    prompt: str


class Masking(Agent):
    """
    This Agent is load from learning phrases and generate a text and mask the phrase and ask the user to fill it.
    Validation will record the success.
    """

    type: str = "masking"  # Setting default value to the Agent's properties
    categories: List[str] = ["test", "learning"]
    subcategories: List[str] = ["masking", "learning_the_phrases"]
    interaction_types: List[str] = ["text"]
    shared_context_field: str = "learning_phrases"
    compatible_interfaces: List[str] = ["web", "telegram"]
    config: Configuration
    db: ClassVar = get_db("agent_session")

    def __init__(self, **data):
        # Call the parent class constructor with the modified data
        super().__init__(**data)

    def user_prompt(
        self,
        user_goal: Goal,
        the_phrase: str,
    ):
        return (
            self.config.prompt.replace("${learning_language}", user_goal.language)
            .replace("${learning_level}", user_goal.level)
            .replace("${learning_context}", user_goal.context)
            .replace("${the_phrase}", the_phrase)
        )

    def does_session_exist(self, user_id: str, goal_id: str) -> bool:
        """
        Check if a session exists for the given user and goal.
        """
        existing_session = self.db.find(
            "masking_agent",
            {"user_id": user_id, "goal_id": goal_id},
            limit=1,
        )
        return bool(existing_session)

    def get_next_learning_phrase(self, user_id: str, goal_id: str) -> str:
        return learning_phrases.get_next_learning_phrases(user_id, goal_id, top=1)[0]

    def store_next_phrase(self, user_id: str, goal_id: str, next_phrase: str):
        existing_session = self.db.find(
            "masking_agent",
            {"user_id": user_id, "goal_id": goal_id},
            limit=1,
        )
        if not existing_session:
            self.db.insert(
                "masking_agent",
                {
                    "user_id": user_id,
                    "goal_id": goal_id,
                    "last_phrase": next_phrase.lower(),
                },
            )
        else:
            self.db.update(
                "masking_agent",
                {
                    "user_id": user_id,
                    "goal_id": goal_id,
                },
                {"$set": {"last_phrase": next_phrase.lower()}},
            )

    def store_next_phrase_and_context(
        self, user_id: str, goal_id: str, next_phrase: str, next_text: str
    ):
        existing_session = self.db.find(
            "masking_agent",
            {"user_id": user_id, "goal_id": goal_id},
            limit=1,
        )
        if not existing_session:
            self.db.insert(
                "masking_agent",
                {
                    "user_id": user_id,
                    "goal_id": goal_id,
                    "last_phrase": next_phrase.lower(),
                    "next_phrase": next_phrase.lower(),
                    "next_text": next_text,
                },
            )
        else:
            self.db.update(
                "masking_agent",
                {
                    "user_id": user_id,
                    "goal_id": goal_id,
                },
                {"$set": {"next_phrase": next_phrase.lower(), "next_text": next_text}},
            )

    def generate_and_mask(self, user_goal: Goal, next_phrase: str):
        # Generate text to be masked
        next_phrase_user_message = Message(
            content=self.user_prompt(
                user_goal,
                next_phrase,
            ),
            role="user",
        )
        model_response_content = self.model_connector.reply(
            messages=[next_phrase_user_message]
        ).content

        # Mask the next_phrase ignoring case
        splitted_phrase = next_phrase.split()
        for split in splitted_phrase:
            pattern = re.compile(re.escape(split), re.IGNORECASE)
            model_response_content = pattern.sub(BLANK_MASK, model_response_content)

        return model_response_content

    def generate_next_masking_text(self, user_id: str, user_goal: Goal) -> str:
        next_phrase = self.get_next_learning_phrase(user_id, user_goal.id)

        max_retries = 5
        for attempt in range(max_retries):
            masked_generated_response = self.generate_and_mask(user_goal, next_phrase)
            if BLANK_MASK in masked_generated_response:
                # Store the next phrase and context
                self.store_next_phrase_and_context(
                    user_id, user_goal.id, next_phrase, masked_generated_response
                )
                return
            else:
                print(
                    f"WARNING: Couldn't find the phrase in the user context (attempt {attempt + 1})"
                )
        raise RuntimeError("Failed to generate masked phrase after 5 attempts.")

    async def generate_next_masking_text_async(self, user_id: str, user_goal: Goal):
        """
        Asynchronous version of generate_next_masking_text.
        This method is intended to be run in an event loop.
        """
        await asyncio.to_thread(self.generate_next_masking_text, user_id, user_goal)

    def retrieve_next_masking_text(self, user_id: str, user_goal: Goal) -> str:
        session = self.db.find(
            "masking_agent",
            {"user_id": user_id, "goal_id": user_goal.id},
            limit=1,
        )
        if not session or not session[0]:
            raise ValueError("No session found for the user and goal.")
        next_text = session[0].get("next_text")
        if not next_text:
            # Wait and check until next_text is available (max 10 seconds, check every 0.5s)
            timeout = 10
            interval = 0.5
            elapsed = 0
            while not next_text and elapsed < timeout:
                time.sleep(interval)
                elapsed += interval
                session = self.db.find(
                    "masking_agent",
                    {"user_id": user_id, "goal_id": user_goal.id},
                    limit=1,
                )
                next_text = (
                    session[0].get("next_text") if session and session[0] else None
                )
            if not next_text:
                raise RuntimeError("next_text is not available after waiting.")

        # Store next_phrase to check it later
        self.store_next_phrase(user_id, user_goal.id, session[0].get("next_phrase"))
        return next_text

    def validate(self, user_id: str, goal_id: str, user_answer: str) -> str:
        session = self.db.find(
            "masking_agent",
            {"user_id": user_id, "goal_id": goal_id},
            limit=1,
        )
        last_phrase = (
            session[0]["last_phrase"]
            if session and session[0] and "last_phrase" in session[0]
            else None
        )

        if not last_phrase:
            raise ValueError("Previous session or last_phrase is not stored!")
        is_correct = last_phrase == user_answer.lower()
        learning_phrases.update_learning_status(
            user_id, goal_id, last_phrase, is_correct
        )
        return last_phrase

    @property
    def model_connector(self):
        return model_proxy.get_connector(self.model_connector_id)

    def start(self, user_id: str, user_goal: Goal) -> List[Message]:
        if not self.does_session_exist(
            user_id, user_goal.id
        ):  # one time initialization
            self.generate_next_masking_text(user_id, user_goal)
        masking_text = self.retrieve_next_masking_text(user_id, user_goal)
        # Prepare next text
        asyncio.run(self.generate_next_masking_text_async(user_id, user_goal))
        # send back the first message with the masked text
        return [
            Message(content=masking_text, role="assistant"),
        ]

    def reply(
        self, user_id: str, user_goal: Goal, messages: List[Message]
    ) -> List[Message]:
        # Validate user answer
        last_phrase = self.validate(user_id, user_goal.id, messages[0].content)
        # Prepare next text
        masking_text = self.retrieve_next_masking_text(user_id, user_goal)
        # Prepare future text asynchronously
        asyncio.run(self.generate_next_masking_text_async(user_id, user_goal))
        return [
            Message(content=last_phrase, role="assistant"),
            Message(content=masking_text, role="assistant"),
        ]
