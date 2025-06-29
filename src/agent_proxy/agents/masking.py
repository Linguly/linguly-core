from src.agent_proxy.types import Agent, Message
from src.model_proxy import model_proxy
from src.shared_context.types import Goal
from src.shared_context.learning_phrases import LearningPhrases
from pydantic import BaseModel, Field
from typing import List
import json

learning_phrases = LearningPhrases()


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

    def get_next_learning_phrase(self, user_id: str, goal_id: str):
        return learning_phrases.get_next_learning_phrases(user_id, goal_id, top=1)

    def generate_next_masking_text(self, user_id: str, user_goal: Goal) -> str:
        next_phrase = self.get_next_learning_phrase(user_id, user_goal.id)[0]
        learning_language = user_goal.language
        masking_user_message = Message(
            content=self.user_prompt(
                user_goal,
                next_phrase,
            ),
            role="user",
        )
        model_response_content = self.model_connector.reply(
            messages=[masking_user_message]
        ).content
        # mask the next_phrase
        splitted_phrase = next_phrase.split()
        for split in splitted_phrase:
            model_response_content = model_response_content.replace(split, "`______`")

        if "`______`" in model_response_content:
            return model_response_content
        else:
            print("WARNING: Couldn't find the phrase in the user context")
            # TODO: proper action required here (e.g. regenerate the text)
            return model_response_content

    @property
    def model_connector(self):
        return model_proxy.get_connector(self.model_connector_id)

    def start(self, user_id: str, user_goal: Goal) -> List[Message]:
        masking_text = self.generate_next_masking_text(user_id, user_goal)
        return [
            Message(content=self.description, role="assistant"),
            Message(content=masking_text, role="assistant"),
        ]

    def reply(
        self, user_id: str, user_goal: Goal, messages: List[Message]
    ) -> List[Message]:
        user_message = messages[0]
        # TODO: validate the answer!

        masking_text = self.generate_next_masking_text(user_id, user_goal)
        # TODO: return previous phrase before sending next text
        return [Message(content=masking_text, role="assistant")]

    def validate(self, user_id: str, user_message: Message, user_goal: Goal):
        # TODO: validate if the user message match the phrase and record the result in learning_phrases + return the phrase
        pass
