from src.model_proxy.types import ModelConnector, Message
from pydantic import BaseModel
from typing import List
import openai
import os
from openai import OpenAI


class Configuration(BaseModel):
    """
    Connector Configuration. Unique per instance.
    """

    api_key_env_var: str
    api_key: str = ""


class Openai(ModelConnector):
    """
    This Connector is to connect to the OpenAI hosted models using a api_key.
    """

    type: str = "openai"  # Setting default value to the Connector's properties
    category: List[str] = ["language_model"]
    interaction_type: List[str] = ["text"]
    config: Configuration

    def __init__(self, **data):
        # Call the parent class constructor with the modified data
        super().__init__(**data)

        api_key_env_var = data.get("config", {}).get("api_key_env_var", None)
        self.config.api_key = os.environ.get(api_key_env_var, "")
        # to check available models:
        # client = OpenAI(api_key=self.config.api_key)
        # print("model list:", client.models.list())

    def form_messages(self, user_prompt: str, system_prompt: str = "") -> List:
        messages = []
        if system_prompt != "":
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return messages

    def chat(self, messages):
        client = OpenAI(api_key=self.config.api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        return response.message.content

    def reply(self, messages: List[Message]) -> Message:
        response = self.chat(messages)
        print(f"OpenAI response: {response}")
        return Message(content=response, role="assistant")
