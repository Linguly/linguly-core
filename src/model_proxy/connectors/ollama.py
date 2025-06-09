# To learn more about ollama APIs, visit https://pypi.org/project/ollama/
from src.model_proxy.types import ModelConnector, Message
from pydantic import BaseModel
from typing import List
from ollama import Client
import os


class Configuration(BaseModel):
    """
    Connector Configuration. Unique per instance.
    """

    api_url_env_var: str
    api_url: str = ""


class Ollama(ModelConnector):
    """
    This Connector is to connect to the ollama based models that will be hosted by Linguly.
    It uses the ollama Python client to interact with the models.
    """

    type: str = "hosted_model"  # Setting default value to the Connector's properties
    category: List[str] = ["language_model"]
    interaction_type: List[str] = ["text"]
    config: Configuration

    def __init__(self, **data):
        # Call the parent class constructor with the modified data
        super().__init__(**data)

        api_url_env_var = data.get("config", {}).get("api_url_env_var", None)
        self.config.api_url = os.environ.get(api_url_env_var, "http://localhost:11434")

    def form_messages(self, user_prompt: str, system_prompt: str = "") -> List:
        messages = []
        if system_prompt != "":
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return messages

    def chat(self, messages):
        client = Client(host=self.config.api_url)
        response = client.chat(
            model=self.model_name,
            messages=messages,
        )
        return response.message.content

    def generate(self, prompt):
        client = Client(host=self.config.api_url)
        output = client.generate(
            model=self.model_name,
            prompt=prompt,
        )
        return output.response

    def reply(self, messages: List[Message]) -> Message:
        response = self.generate(messages[0].content)
        return Message(content=response, role="assistant")
