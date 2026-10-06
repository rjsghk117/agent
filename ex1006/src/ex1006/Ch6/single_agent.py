# Tavily Search를 이용한 웹 검색
from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=2)
result = tool.invoke({"query": "What is a Langgraph?"})
# print(result)

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
# 함수 선언 아랫줄에 docstring을 통해 간단히 도구의 설명을 작성
# 이 설명 텍스트는 실제로 도구 호출에 사용되므로 꼼꼼히 작성해두는 것이 좋음
tools = [add, multiply]

# -------------------------------------------

# 도구 호출을 위한 bind_tools 사용하기
# bind_tools는 랭체인 채팅 모델이 구현하는 메서드로, 도구가 필요한 경우 도구 호출을 하게 함

# LLM에게 사용할 도구 쥐어주기
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# 도구의 사용이 필요한 질문 입력하기
query = "What is 3 times 5? Also, what is 2 plus 4?"

response = llm_with_tools.invoke(query)
# print(response)
# content='' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 50, 'prompt_tokens': 113, 'total_tokens': 163, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_02e43187ba', 'id': 'chatcmpl-EVporSoUgPTkfZGVudqen0IAMpGAo', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None} id='lc_run--01a10f2e-7889-7483-b0bf-86dd1a132d02-0' tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 5}, 'id': 'call_JAEyMWattkkDtYACEn7jw7XT', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 2, 'b': 4}, 'id': 'call_yAGZMZ1ul9f2Aw19a5xyOQt3', 'type': 'tool_call'}] invalid_tool_calls=[] usage_metadata={'input_tokens': 113, 'output_tokens': 50, 'total_tokens': 163, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

# content 속성(attribute)은 비워져 있지만 additional_kwargs의 딕셔너리 내부를 확인하면 tool_calls 키를 확인 가능

# tool_calls로 도구 호출 결과 확인하기
# print(response.tool_calls)
#   [{'name': 'multiply', 
# 'args': {'a': 3, 'b': 5}, 
# 'id': 'call_oykvTk0ehgPsIB7kn3urljuK', 
# 'type': 'tool_call'}, 
#   {'name': 'add', 
# 'args': {'a': 2, 'b': 4}, 
# 'id': 'call_N91SZ7q0qPRG0Bh4uzxNnUNb', 
# 'type': 'tool_call'}]

# 결과가 딕셔너리 리스트에 담겨 있음

# ----------------------------------------

# 도구 사용이 필요 없는 질문 입력하기
query = "Hello!"

response = llm_with_tools.invoke(query)
# print(response)
# content='Hello! How can I assist you today?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 10, 'prompt_tokens': 97, 'total_tokens': 107, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_02e43187ba', 'id': 'chatcmpl-EVq0nyCeUstvNUJsqHN3GCwfmruQs', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--01a10f39-cc45-7543-9c40-03548e6cbe50-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 97, 'output_tokens': 10, 'total_tokens': 107, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# 도구 호출이 이러우지지 않았으니 tool_calls는 빈 리스트를 반환

# 빈 리스트 반환하는 결과 확인하기
# print(response.tool_calls)
# []

# ---------------------------------------
# Tavily Search 도구를 바인딩한 모델 사용하기

# 웹 검색 도구를 사용하는 LLM 모델 만들기
from langchain_openai import ChatOpenAI

tool = TavilySearch(max_results=2)
tools = [tool]

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke("What is the latest trend of AI in 2026?")
# print(response)
# content='' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 31, 'prompt_tokens': 1199, 'total_tokens': 1230, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 1024, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_0ae67b3da2', 'id': 'chatcmpl-EVq8rxkyFSF6SKmXCoQegiAkxHQWj', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None} id='lc_run--01a10f41-6d79-7fb3-8f7a-eac0c199b8dd-0' tool_calls=[{'name': 'tavily_search', 'args': {'query': 'latest AI trends in 2026', 'time_range': 'year', 'topic': 'general'}, 'id': 'call_TV6tzTuDJZAK3XibnwkcXB15', 'type': 'tool_call'}] invalid_tool_calls=[] usage_metadata={'input_tokens': 1199, 'output_tokens': 31, 'total_tokens': 1230, 'input_token_details': {'audio': 0, 'cache_read': 1024}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

# print(response.tool_calls)
# [{'name': 'tavily_search', 
# 'args': {'query': 'latest AI trends 2026', 
# 'time_range': 'year', 'topic': 'news'}, 
# 'id': 'call_x4cBpDKIuiGJvMwlLVUIdC0q', 
# 'type': 'tool_call'}]

# 실제로 도구를 실행한 것이 아니라, LLM이 사용자의 질문을 바탕으로 필요한 도구를 판단하는 단계까지만 수행

# ----------------------------------------------------------------------------------------

# 6.2.3 Langgraph로 Agent Graph 생성
# Tavily Search 도구 및 LLM 설정
# 도구 바인딩 모델을 생성

# Tavily Search 도구를 사용하는 LLM 만들기
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=3)
tools = [tool]

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)