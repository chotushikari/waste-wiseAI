# agents/memory.py

from langchain.memory import ConversationBufferMemory

def get_conversation_memory():
    """
    Memory for tracking full conversation history.
    Used to give multi-turn intelligence to the agent.
    """
    return ConversationBufferMemory(return_messages=True)
