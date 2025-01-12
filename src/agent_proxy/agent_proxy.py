from typing import List
from src.agent_proxy.types import Message
from src.agent_proxy.agents.dictionary import Dictionary


# initialize agents
dictionary = Dictionary(id="1_dictionary", display_name="dictionary_1", config={"card_fields":[{"name": "In English","description":"translate"}]})

def get_available_agents():
    return [{"id": "1_dictionary", "type": "dictionary", "display_name": "dictionary_1"}]

def get_selected_agent(agent_id: str):
    return dictionary

def message_agent(agent_id: str, user_message: Message):
    agent = get_selected_agent(agent_id)
    return agent.reply(user_message)
    
    
    
print(message_agent(agent_id="1_dictionary", user_message = Message(content= "test") ))