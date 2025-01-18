
from src.model_proxy.types import ModelConnector, Message
from pydantic import BaseModel
from typing import List

class Configuration(BaseModel):
    """
    Connector Configuration. Unique per instance.
    """
    api_url: str
    

class BasicModel(ModelConnector):
    """
    This Connector is to connect to the basic models that will be hosted by Linguly.
    Also known as the simple connector that can be connected to any open access hosted model with the minimalistic interactions.
    """
    type: str = "hosted_model" # Setting default value to the Connector's properties
    category: List[str] = ["language_model"]
    interaction_type: List[str] = ["text"]
    config: Configuration
    
    def __init__(self, **data):
        # Modify the config structure
        if "configuration" in data:
            data["config"] = data["config"]

        # Call the parent class constructor with the modified data
        super().__init__(**data)
        
    def reply(self, user_message: Message) -> Message:
        return Message(content = """{
"translation": "training",
"synonyms": [
"education",
"instruction"
],
"example": "She is undergoing training to learn her new job."
}""")