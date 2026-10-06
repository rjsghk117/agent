# Tavily Search를 이용한 웹 검색
from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=2)
result = tool.invoke({"query": "What is a Langgraph?"})
print(result)

# {'query': 'What is a Langgraph?', 
# 'follow_up_questions': None, 
# 'answer': None, 'images': [], 
# 'results': [{'url': 'https://www.geeksforgeeks.org/machine-learning/what-is-langgraph', 'title': 'What is LangGraph - GeeksforGeeks', 'content': 'LangGraph is an open-source framework from LangChain designed to build and manage AI agent workflows using graph-based structures. It allows developers to define workflows as nodes and edges, making complex agent interactions more structured, scalable and easier to control. [...] langgraph: Framework for building graph-based AI workflows.\n langchain: Popular toolkit for LLM-powered AI applications.\n google-generativeai: Google’s API for Generative AI (Gemini models).\n\n Python  ````\n! pip install langgraph langchain google - generativeai\n```` \n\n### Step 2: Setup Gemini API [...] ## Building a Simple Chatbot with LangGraph\n\nLangGraph makes it easy to build structured, stateful applications like chatbots. In this example we’ll learn how to create a basic chatbot that can classify user input as either a greet, search query and respond accordingly.\n\n### Step 1: Install the Dependencies\n\nInstalls the required dependencies,', 
# 'score': 0.95386744, 
# 'raw_content': None, 'id': 'd0f972-00'}, 
# {'url': 'https://www.ibm.com/think/topics/langgraph', 
# 'title': 'What is LangGraph? | IBM', 
# 'content': 'LangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\n\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences. [...] LangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis.', 
# 'score': 0.9466806, 'raw_content': None, 'id': '8686f7-01'}], 
# 'response_time': 0.0, 'request_id': '0e3fbd99-b255-4472-9e27-6fe1e3ec1aad'}

# ----------------------------------------

# 랭체인 기반 도구 만들기
# 직접 덧셈과 곱셈 도구 만들기
from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Adds a and b.
    
    Args: 
        a: first int
        b: second int
    """
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.
    
    Args:
        a: first int
        b: second int
    """
    return a * b

tools = [add, multiply]