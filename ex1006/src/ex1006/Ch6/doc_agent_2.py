from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.tools import tool
load_dotenv()

class Answer(BaseModel):
    summary: str
    confidence: float

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search],
    response_format=Answer,
    system_prompt="You are a study assistant. Give only the core ideas and make it simple."
)

result = agent.invoke({"messages": [{"role": "user", "content": "Please explain what a single agent is."}]})
# print(result["structured_response"])
# summary='A single agent is one system or entity that acts on its own to achieve a goal. It observes its environment, makes decisions, and takes actions. For example, a robot vacuum is a single agent: it senses dirt or obstacles, decides where to move, and cleans the floor. In AI, a single agent does not need to coordinate with other agents; it focuses only on its own task and choices.' confidence=0.98