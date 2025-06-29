from typing import List
from src.model_proxy.types import Message
from src.model_proxy.connectors.echo import Echo
from src.model_proxy.connectors.ollama import Ollama
from src.model_proxy.connectors.openai import Openai
import yaml
import os


def load_config():
    with open("src/model_proxy/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def init_connectors():
    """
    Initialize the model connectors based on the loaded configuration.

    This function should be called to set up the model connectors
    using the configuration loaded from the YAML file.
    """
    config = load_config()
    available_connectors = []
    for connector in config.get("model_connectors", []):
        # Initialize each database connection here
        connector_type = connector.get("type")
        if connector_type == "echo":
            available_connectors.append(
                Echo(
                    id=connector.get("id"),
                    display_name=connector.get("display_name"),
                    model_name=connector.get("model_name"),
                    supported_languages=connector.get("supported_languages", []),
                )
            )
        elif connector_type == "ollama":
            available_connectors.append(
                Ollama(
                    id=connector.get("id"),
                    display_name=connector.get("display_name"),
                    model_name=connector.get("model_name"),
                    config=connector.get("config", {}),
                    supported_languages=connector.get("supported_languages", []),
                )
            )
        elif connector_type == "openai":
            available_connectors.append(
                Openai(
                    id=connector.get("id"),
                    display_name=connector.get("display_name"),
                    model_name=connector.get("model_name"),
                    config=connector.get("config", {}),
                    supported_languages=connector.get("supported_languages", []),
                )
            )
        else:
            print(f"Unsupported model connector type: {connector_type}")
    if not available_connectors:
        print("No model connector available. Please check your configuration.")
    return available_connectors


def get_available_connectors():
    return available_connectors


def get_connector(connector_id: str):
    """
    Retrieve a model connector by its ID.

    Args:
        connector_id (str): The ID of the connector to retrieve.

    Returns:
        ModelConnector: The model connector instance.
    """
    # Always echo the input if echo mode is enabled to reduce cost and complexity when testing
    echo_mode = os.environ.get("ECHO_MODEL_ENABLED", 'false')
    if echo_mode == 'true':
        connector_id = "echo"

    # Find and return the selected connector
    for connector in available_connectors:
        if connector.id == connector_id:
            return connector
    print(f"Model connector with id {connector_id} not found.")
    return None


available_connectors = init_connectors()
