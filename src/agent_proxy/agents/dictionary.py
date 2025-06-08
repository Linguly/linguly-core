from src.agent_proxy.types import Agent, Message
from src.model_proxy import model_proxy
from pydantic import BaseModel, Field
from typing import List
import json


class CardField(BaseModel):
    name: str = Field(..., description="Field Name")
    description: str = Field(None, description="Field Description")


class Configuration(BaseModel):
    """
    Agent Configuration. Unique per instance.
    """

    card_fields: List[CardField]


class Prompt:
    def card_fields_str(card_fields: List[CardField]):
        return "\n".join(
            [f'"{field.name}": "{field.description}", ' for field in card_fields]
        )

    def user(
        self,
        to_learn_language: str,
        base_language: str,
        card_fields: List[CardField],
        user_message: str,
    ):
        return f"""You are a dictionary and give me the following output fields based on the given inputs.
The output should be in json format with no additional text and information:
    
# inputs
phrase= {user_message}
    
# outputs
{{
{self.card_fields_str(card_fields).replace("to_learn_language", to_learn_language).replace("base_language", base_language)}
}}
"""


class Dictionary(Agent):
    """
    This Agent is to take a word or phrase and return a dictionary card showing requested information in the configuration
    """

    type: str = "dictionary"  # Setting default value to the Agent's properties
    category: List[str] = ["tool"]
    interaction_type: List[str] = ["card"]
    shared_context_field: str = "learning_phrases"
    config: Configuration

    # temporary hard coded fields (will come from the user goals)
    to_learn_language: str = "German"
    base_language: str = "English"

    def __init__(self, **data):
        # Modify the config structure
        if "configuration" in data:
            data["config"] = data["config"]

        # Call the parent class constructor with the modified data
        super().__init__(**data)

    @property
    def model_connector(self):
        return model_proxy.get_connector(self.model_connector_id)

    # Asking for a json output and then formatting it here can help us receiving more reliable output format from the model
    def format_output(self, output_str: str) -> str:
        print(output_str)
        try:
            output_json = json.loads(output_str)
            formatted_output = "\n".join(
                f"{key}: {value}" for key, value in output_json.items()
            )
        except json.JSONDecodeError as e:
            formatted_output = (
                "Invalid response from the model. Please try again! \n Model response: \n"
                + output_str
            )
        return formatted_output

    def reply(self, user_message: Message) -> List[Message]:
        user_message = Message(
            content=Prompt.user(
                Prompt,
                self.to_learn_language,
                self.base_language,
                self.config.card_fields,
                user_message.content,
            ),
            role="user",
        )
        model_response = self.model_connector.reply(messages=[user_message])
        model_response.content = self.format_output(model_response.content)
        return model_response
