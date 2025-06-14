from src.agent_proxy.types import Agent, Message
from src.model_proxy import model_proxy
from src.shared_context.types import Goal
from src.shared_context.learning_phrases import LearningPhrases
from pydantic import BaseModel, Field
from typing import List
import json

learning_phrases = LearningPhrases()

class CardField(BaseModel):
    name: str = Field(..., description="Field Name")
    description: str = Field(None, description="Field Description")


class Configuration(BaseModel):
    """
    Agent Configuration. Unique per instance.
    """

    card_fields: List[CardField]


class Prompt(BaseModel):
    def card_fields_str(self, card_fields: List[CardField]):
        return "\n".join([f"- {field.description}" for field in card_fields])

    def user(
        self,
        learning_language: str,
        card_fields: List[CardField],
        user_message: str,
    ):
        return (
            f"Give me the requested information in {learning_language} with a super short and direct answer:\n"
            f"{self.card_fields_str(card_fields).replace('learning_language', learning_language).replace('the_phrase', user_message)}"
        )


class Dictionary(Agent):
    """
    This Agent is to take a word or phrase and return a dictionary card showing requested information in the configuration
    """

    type: str = "dictionary"  # Setting default value to the Agent's properties
    categories: List[str] = ["tool", "learning"]
    subcategories: List[str] = ["dictionary", "add_to_learning_phrases"]
    interaction_types: List[str] = ["text"]
    shared_context_field: str = "learning_phrases"
    compatible_interfaces: List[str] = ["web", "telegram"]
    config: Configuration
    prompt: Prompt = Prompt()

    def __init__(self, **data):
        # Call the parent class constructor with the modified data
        super().__init__(**data)
        
    def add_to_learning_phrases(self, phrase: str, user_id: str, goal_id: str):
        learning_phrases.add_to_learning_phrases([phrase], user_id, goal_id, source_id=self.id, source_type='agent')
        

    @property
    def model_connector(self):
        return model_proxy.get_connector(self.model_connector_id)

    def reply(
        self, user_id: str, user_message: Message, user_goal: Goal
    ) -> List[Message]:
        self.add_to_learning_phrases(user_message.content, user_id, user_goal)
        learning_language = user_goal.language
        dictionary_user_message = Message(
            content=self.prompt.user(
                self.learning_language,
                self.config.card_fields,
                user_message.content,
            ),
            role="user",
        )
        model_response = self.model_connector.reply(messages=[dictionary_user_message])
        return user_message
