from typing import List
from src.agent_proxy.types import Message
from src.agent_proxy.agents.dictionary import Dictionary


# initialize agents
dictionary = Dictionary(id="1_dictionary", display_name="dictionary_1", model_connector_id="1_connector", config={"card_fields":[{"name": "In English","description":"translate"}]})
available_agents = [dictionary]

def get_available_agents():
    agents_metadata = []
    for agent in available_agents:
        agents_metadata.append({
            "id": agent.id,
            "type": agent.type,
            "display_name": agent.display_name,
            "category": agent.category,
            "interaction_type": agent.interaction_type,
            "model_connector_id": agent.model_connector_id
        })
    return agents_metadata

def get_agent(agent_id: str):
    for agent in available_agents:
        if agent.id == agent_id:
            return agent
    raise ValueError(f"Agent with id {agent_id} not found")

def message_agent(agent_id: str, user_message: Message):
    agent = get_agent(agent_id)
    return agent.reply(user_message)
    