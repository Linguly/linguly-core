from typing import List
from src.agent_proxy.types import Message, Agent
from src.model_proxy import model_proxy
from src.agent_proxy.agents.dictionary import Dictionary
from src.agent_proxy.agents.masking import Masking
from src.shared_context.goals import Goals
import yaml

goals = Goals()


def load_config():
    with open("src/agent_proxy/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def get_model_supported_languages(model_connector_id: str):
    model_connector = model_proxy.get_connector(model_connector_id)
    return model_connector.supported_languages


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
                    supported_languages=get_model_supported_languages(
                        agent.get("model_connector_id")
                    ),
                )
            )
        elif agent_type == "masking":
            available_agents.append(
                Masking(
                    id=agent.get("id"),
                    display_name=agent.get("display_name"),
                    model_connector_id=agent.get("model_connector_id"),
                    description=agent.get("description"),
                    config=agent.get("config", {}),
                    supported_languages=get_model_supported_languages(
                        agent.get("model_connector_id")
                    ),
                )
            )
        else:
            print(f"Unsupported agent type: {agent_type}")
    if not available_agents:
        print("No agent available. Please check your configuration.")
    return available_agents


def get_available_agents(user_id: str) -> List[Agent]:
    user_goal = goals.get_selected_goal(user_id)
    agents_metadata = []
    for agent in available_agents:
        # Include only agents that their supported languages is including user's goal
        if user_goal.language in agent.supported_languages:
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
                    supported_languages=agent.supported_languages,
                )
            )
    return agents_metadata


def get_agent(agent_id: str):
    for agent in available_agents:
        if agent.id == agent_id:
            return agent
    raise ValueError(f"Agent with id {agent_id} not found")


def start_the_agent(agent_id: str, user_id: str) -> List[Message]:
    agent = get_agent(agent_id)
    print(f"Start agent: {agent.display_name} ({agent.id})")
    user_goal = goals.get_selected_goal(user_id)
    return agent.start(user_id, user_goal)


def chat_with_agent(
    agent_id: str, user_id: str, messages: List[Message]
) -> List[Message]:
    agent = get_agent(agent_id)
    print(f"Chat with agent: {agent.display_name} ({agent.id})")
    user_goal = goals.get_selected_goal(user_id)
    return agent.reply(user_id, user_goal, messages)


available_agents = init_agents()
