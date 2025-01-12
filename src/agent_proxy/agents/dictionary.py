
from src.agent_proxy.types import Agent, Message
from pydantic import BaseModel, Field
from typing import List

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
        return '\n'.join([f"{field.name}: //{field.description} " for field in card_fields])
    
    def user(self, to_learn_language: str, base_language: str, card_fields: List[CardField], user_message: str):
        return f"""You are a dictionary and give me the following output fields based on the given inputs.
The output should be in json format with no additional text and information:
    
# inputs
phrase= {user_message}
to_learn_language= {to_learn_language}
base_language= {base_language}
    
# outputs
{self.card_fields_str(card_fields).replace("to_learn_language", to_learn_language).replace("base_language", base_language)}
    """

class Dictionary(Agent):
    """
    This Agent is to take a word or phrase and return a dictionary card showing requested information in the configuration
    """
    type: str = "dictionary" # Setting default value to the Agent's properties
    category: List[str] = ["tool"]
    interaction_type: List[str] = ["card"]
    shared_context_field: str = "to_learn_phrases"
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
        
    def reply(self, user_message: Message) -> List[Message]:
        return [Message(content = Prompt.user(Prompt, self.to_learn_language, self.base_language, self.config.card_fields, user_message.content))]