from typing import List
from src.agent_proxy.types import Message, Agent
from src.agent_proxy.agents.dictionary import Dictionary
import yaml


def load_config():
    with open("src/agent_proxy/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def init_agents():
    """
    Initialize the agents based on the loaded configuration.

    This function should be called to set up the agents
    using the configuration loaded from the YAML file.
    """
    config = load_config()
    available_agents = []
    for agent in config.get("agents", []):
        # Initialize each agent here
        agent_type = agent.get("type")
        if agent_type == "dictionary":
            available_agents.append(
                Dictionary(
                    id=agent.get("id"),
                    display_name=agent.get("display_name"),
                    model_connector_id=agent.get("model_connector_id"),
                    description=agent.get("description"),
                    config=agent.get("config", {}),
                )
            )
        else:
            print(f"Unsupported agent type: {agent_type}")
    if not available_agents:
        print("No agent available. Please check your configuration.")
    return available_agents


def get_available_agents() -> List[Agent]:
    agents_metadata = []
    for agent in available_agents:
        agents_metadata.append(
            Agent(
                id=agent.id,
                type=agent.type,
                display_name=agent.display_name,
                categories=agent.categories,
                subcategories=agent.subcategories,
                description=agent.description,
                interaction_types=agent.interaction_types,
                model_connector_id=agent.model_connector_id,
                compatible_interfaces=agent.compatible_interfaces,
            )
        )
    return agents_metadata


def get_agent(agent_id: str):
    for agent in available_agents:
        if agent.id == agent_id:
            return agent
    raise ValueError(f"Agent with id {agent_id} not found")


def message_agent(agent_id: str, user_message: Message):
    agent = get_agent(agent_id)
    print(f"Using agent: {agent.display_name} ({agent.id})")
    return agent.reply(user_message)


available_agents = init_agents()
