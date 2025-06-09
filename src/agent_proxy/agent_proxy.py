from typing import List
from src.agent_proxy.types import Message, Agent
from src.agent_proxy.agents.dictionary import Dictionary


# initialize agents (soon to be loaded from a yaml file/db)
dictionary = Dictionary(
    id="1_dictionary",
    display_name="Dictionary + add to learning phrases",
    model_connector_id="basic_llama_connector",
    description="""This agent is to take a word or phrase and return a dictionary card showing a list of information.
It always adds the phrase to the learning phrases list of the selected learning goal.""",
    config={
        "card_fields": [
            {
                "name": "Translation",
                "description": "translate the phrase into base_language",
            },
            {"name": "Synonyms", "description": "few synonyms in to_learn_language"},
            {
                "name": "Example",
                "description": "at least two sentences using the phrase in to_learn_language",
            },
            {
                "name": "Definition",
                "description": "definition of the phrase in to_learn_language",
            },
        ]
    },
)
available_agents = [dictionary]


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
    print(f"Message to agent {agent_id}: {user_message.content}")
    agent = get_agent(agent_id)
    print(f"Using agent: {agent.display_name} ({agent.id})")
    return agent.reply(user_message)


# print(message_agent("1_dictionary", Message(content="ausrede", role="user")))
