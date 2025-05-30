from typing import List
from src.model_proxy.types import Message
from src.model_proxy.connectors.basic_model import BasicModel
import os


# initialize connectors
basic_model = BasicModel(
    id="1_connector",
    display_name="llama3.2_3B_linguly_live",
    config={"api_url": os.environ["BASIC_MODEL_URL"]},
    model_name="llama3.2:3b",
    supported_languages=[
        "English",
        "German",
        "French",
        "Italian",
        "Portuguese",
        "Hindi",
        "Spanish",
        "Thai",
    ],
)


def get_available_connectors():
    return [
        {
            "id": "1_connector",
            "type": "basic_model",
            "display_name": "llama3.2_3B_linguly_live",
        }
    ]


def get_connector(connector_id: str):
    return basic_model


def message_model(connector_id: str, messages: List[Message]):
    model_connector = get_connector(connector_id)
    return model_connector.reply(messages)


print(basic_model.config)
