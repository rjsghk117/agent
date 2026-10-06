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

# -----------------------------------------

# 상태 그래프 생성
# 간단히 메시지만 주고받으며 관리할 수 있도록 "messages" 키를 가지는 데이터 스키마를 만듦
# 노드가 새로운 메시지를 업데이트할 때마다 누적될 수 있도록 add_messages 리듀서 함수를 사용

# 메세지 목록을 관리하는 그래프 상태 정의하고 상태 그래프 만들기
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# --------------------------------------------------

# 노드 생성하기 (LLM 노드)
# 우선 사용자의 질문을 받는 LLM 노드가 있어야 함
# 이 노드에서는 LLM이 도구 호출을 판단하며 도구 호출이 발생했다면 조건부 엣지에 의해 실제로 Tavily Search 도구를 실행하는 노드로 보내줌
# 실행이 완료되면 웹 검색 결과를 다시 LLM 노드가 받아 답변을 생성하여 종료할 수 있음
# 만약 한 번의 도구 실행으로 답변이 완료되지 않는다면 남은 작업을 처리하기 위해 LLM 노드는 도구 호출을 다시 발생시켜 답변이 가능해질 때까지 이 과정을 반복 할 수 있음

# LLM의 답변을 생성하는 노드 만들기
def chatbot(state: State): # chatbot 이라는 함수로 노드를 구현
    response = llm_with_tools.invoke(state["messages"]) 
    # 도구 바인딩 모델을 사용하며, 상태의 "messages" 값을 입력으로 받아 메시지에 대한 처리를 진행
    # 모델의 결과 메시지는 response에 저장되고, 함수의 반환값을 통해 상태 업데이트를 진행
    return {"messages": response}

graph_builder.add_node("chatbot", chatbot)

# --------------------------------------------------

# 노드 생성하기
# 도구를 실행하고 실행 결과를 저장하는 노드를 구현

# LLM이 호출한 도구를 실행하는 노드 만들기
import json
from langchain.messages import ToolMessage

class BasicToolNode:
    """
        마지막 AIMessage에서 요청된 도구를 실행하는 노드
    """

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    # chatbot 노드에서 업데이트된 도구 호출 결과를 확인하기 위해 마지막 메시지 불러옴
    # 이 메시지는 AIMessage로, tool_calls 속성을 가짐
    # 해당 속성의 값을 도구의 입력으로 사용해 도구를 실행할 수 있음
    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("ERROR: 입력에 메시지가 없습니다.")

        # 마지막 메시지의 tool_calls 속성을 확인하고, 호출된 도구를 불러와 도구 호출에 반환된 인자를 입력해 실행(invoke)함
        # 도구 실행 결과는 tool_result에 저장되고, 이를 도구 메시지로 변환해 메시지 업데이트를 준비
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            # 도구 메시지는 랭체인의 ToolMessage를 사용해 생성할 수 있음
            # ToolMessage의 파라미터는 content를 기본으로 가지며, 여기에는 도구 실행 결과가 들어감
            # 이 외에 도구의 이름과 도구 호출의 id를 입력
            # 이때 id는 chatbot 노드에서 생성된 AIMessage의 도구 호출 id를 사용함
            # 도구 메시지를 생성했다면 "messages" 키에 업데이트하며 노드가 종료
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result, ensure_ascii=False),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"]
                )
            )
        return {"messages": outputs}

tool_node = BasicToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# ---------------------------------------------

# 엣지 생성하기(조건부 흐름 구성)
# 노드를 만들었으니 이를 연결할 엣지를 추가할 차례
# chatbot 노드에서 도구 호출이 발생했다면 도구 실행 노드로 라우팅하고, 그렇지 않으면 END로 라우팅하여 에이전트가 종료되도록 조건부 엣지 구현
# chatbot 노드로부터 업데이트된 마지막 메시지를 확인하고, 해당 메시지에 tool_calls의 결과가 존재하다면 도구를 실행하도록 구현
# 먼저 현재 그래프의 상태를 입력받아 마지막 메시지를 불러옴
# 그리고 다음과 같은 조건문을 통해 도구 호출이 발생했는지를 확인
# - hasattr(ai_message, "tool_calls"): tool_calss 속성이 존재하는지 여부
# - len(ai_message.tool_calls) > 0: tool_calls 속성이 비어 있지 않은지 여부
# 두 가지 조건을 모두 충족해야 도구 호출이 정상적으로 이루어진 것이므로, 이 경우 "tools"를 반환함
# 그렇지 않으면 END를 반환
# 이 함수로 add_conditional_edges를 통해 조건부 엣지를 추가할 때 "tools"를 반환했다면 앞에서 추가한 tools 노드로 이동할 수 있도록 설정

# LLM의 도구 호출 겨로가에 따라 처리하는 조건부 엣지 만들기
def route_tools(
        state: State,
):
    """
    마지막 메시지에 도구 호출이 있는 경우, ToolNode로 라우팅하고 그렇지 않으면 END로 라우팅
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"ERROR: 입력에 메시지가 없습니다. 상태: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END}
)

# ------------------------------------

# 엣지 생성 및 그래프 컴파일하기
# 도구 실행 후 다시 chatbot 노드로 들어가는 엣지와 시작점에서 chatbot 노드로 들어가는 엣지 추가
# 그리고 그래프를 컴파일하여 컴파일된 상태그래프를 생성하면 완료
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

# -----------------------------------

# 6.2.4 최신 정보 검색하고 답변 받아보기
# 그래프를 시각화하여 저장하고 실행하기
# invoke 사용하기
if __name__ == "__main__":
    try:
        image = graph.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(image)
    except Exception:
        pass

    response = graph.invoke(
        {
            "messages": ["Langgraph가 무엇인가요?"]
        }
    )

# print(response)
# content='' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 26, 'prompt_tokens': 1199, 'total_tokens': 1225, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_0ae67b3da2', 'id': 'chatcmpl-EVtCK3MDHN8uhw8Ol0sy1BpUkuePk', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None} id='lc_run--01a10ff4-adc0-7930-a2d2-7773c1f7bae7-0' tool_calls=[{'name': 'tavily_search', 'args': {'query': 'AI trends in 2026', 'time_range': 'year'}, 'id': 'call_pL3I1stBfd2OpImEjkQWHgqm', 'type': 'tool_call'}] invalid_tool_calls=[] usage_metadata={'input_tokens': 1199, 'output_tokens': 26, 'total_tokens': 1225, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

# pretty_print()를 사용해 메시지 목록 출력하기
def invoke():
    response = graph.invoke(
        {
            "messages": ["Langgraph가 무엇인가요?"]
        }
    )

    for msg in response["messages"]:
        msg.pretty_print()

if __name__ == "__main__":
    invoke()

# print(invoke())
# ================================ Human Message =================================

# Langgraph가 무엇인가요?
# ================================== Ai Message ==================================
# Tool Calls:
#   tavily_search (call_Wpqi6NIOBilPYrxgIGtoRxkr)
#  Call ID: call_Wpqi6NIOBilPYrxgIGtoRxkr
#   Args:
#     query: Langgraph
# ================================= Tool Message =================================
# Name: tavily_search

# {"query": "Langgraph", "follow_up_questions": null, "answer": null, "images": [], "results": [{"url": "https://www.ibm.com/think/topics/langgraph", "title": "What is LangGraph? | IBM", "content": "LangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\n\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences. [...] LangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis.", "score": 0.933969, "raw_content": null, "id": "e0784d-00"}, {"url": "https://academy.langchain.com/courses/intro-to-langgraph", "title": "Foundation: Introduction to LangGraph - Python", "content": "No. LangGraph is an orchestration framework for complex agentic systems and is more low-level and controllable than LangChain agents. On the other hand, LangChain provides a standard interface to interact with models and other components, useful for straight-forward chains and retrieval flows.\n How is LangGraph different from other agent frameworks? [...] Other agentic frameworks can work for simple, generic tasks but fall short for complex tasks bespoke to a company’s needs. LangGraph provides a more expressive framework to handle companies’ unique tasks without restricting users to a single black-box cognitive architecture.\n Does LangGraph impact the performance of my app?  \n\n  LangGraph will not add any overhead to your code and is specifically designed with streaming workflows in mind.\n Is LangGraph open source? Is it free? [...] Yes. LangGraph is an MIT-licensed open-source library and is free to use.\n What is LangSmith Deployment?  \n\n  LangSmith Deployment helps you ship your agent in one click, using scalable infrastructure built for long-running tasks.\n\n## Ready to start shipping reliable agents faster?\n\nOur platform provides tools for every step of the agent development lifecycle — built to unlock powerful AI in production.\n\nContact Sales\n\n## Learn with the community", "score": 0.8747745, "raw_content": null, "id": "8ea693-01"}, {"url": "https://medium.com/@tahirbalarabe2/%EF%B8%8Flangchain-vs-langgraph-a-comparative-analysis-ce7749a80d9c", "title": "⚙️LangChain vs. LangGraph: A Comparative Analysis | by Tahir | Medium", "content": "LangGraph is ideal for complex systems that require continuous interaction and adaptation. This includes applications like virtual assistants that need to maintain conversation context over extended periods and manage various user requests. Its stateful nature and flexible graph structure make it suitable for these scenarios where the flow of the application is not linear. [...] LangGraph, on the other hand, is designed for more complex, stateful workflows. It’s a specialized library within the LangChain ecosystem, tailored for building multi-agent systems that handle nonlinear processes.\n\nConsider a task management assistant. The workflow here isn’t linear. It involves processing user input, adding tasks, completing tasks, and summarizing tasks. LangGraph models this as a graph structure, where each action is a node and the transitions between actions are edges. [...] LangGraph is the better choice for applications that need to maintain context and remember past interactions. This is because of its state management, where the state is a core component that all nodes can access and modify. While LangChain can pass data through the chain, it doesn’t have a persistent state feature, making it less suitable for applications requiring memory across multiple runs or dynamic workflow adjustments based on past interactions.\n\nLangchain Vs Langgraph", "score": 0.8732259, "raw_content": null, "id": "f52e50-02"}], "response_time": 0.0, "request_id": "7c7409f4-89ea-4fd6-bd67-fb229903b5c3"}
# ================================== Ai Message ==================================

# LangGraph는 LangChain에 의해 개발된 오픈 소스 AI 에이전트 프레임워크로, 복잡한 생성 AI 에이전트 워크플로우를 구축, 배포 및 관리하기 위해 설계되었습니다. 이를 통해 사용자들은 대형 언어 모델(LLM)을 규모에 맞춰 효율적으로 생성하고 최적화할 수 있습니다. LangGraph는 그래프 기반의 아키텍처를 사용하여 AI 에이전트 워크플로우 내의 다양한 요소 간의 복잡한 관계를 모델링하고 관리합니다.

# LangGraph는 특히 복합 에이전트 시스템 구축에 적합하며, 비선형 프로세스를 처리하는 다중 에이전트 시스템 구축에 특화되어 있습니다. 이는 가상 비서와 같이 긴 시간 동안 대화 컨텍스트를 유지해야 하거나 다양한 사용자 요청을 관리해야 하는 복잡한 시스템에 유리합니다.

# 또한 LangGraph는 오픈 소스로 MIT 라이센스를 통해 무료로 제공됩니다. 이를 통해 기업은 고유하고 복잡한 작업에 맞춘 표현력 있는 프레임워크를 활용할 수 있으며, LangGraph의 상태 관리 기능 덕분에 과거의 상호작용에 대한 기억을 유지할 수 있습니다.
# None

# -----------------------------------------------------------------------------

# ainvoke 사용하기 (비동기 방식)
# ainvoke()를 사용해 실행 결과 확인하기
async def ainvoke():
    response = await graph.ainvoke(
        {
            "messages": ["Langgraph가 무엇인가요?"]
        }
    )

    for msg in response["messages"]:
        msg.pretty_print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(ainvoke())

# 동기 요청 처리
# - 장점: 한 번에 하나의 요청을 처리하므로 그래프의 작업 흐름을 명확하고 쉽게 추적할 수 있음
# - 단점: 여러 요청을 동시에 처리하지 못하고 결과를 받기까지 코드 실행이 멈추므로 시스템의 지연이 발생할 수 있음

# 비동기 요청 처리
# - 장점: 여러 요청을 동시에 처리할 수 있어 대규모 요청이 용이함
# - 단점: 다른 작업을 병렬로 수행하여 작업 흐름을 추적하는데 어려움이 생길 수 있음

# ----------------------------------------------------------------------------
# stream: updates 모드 사용하기
# 기본 값인 updates 모드, 각 노드의 상태 업데이트만 출력되는 방식, 각 노드가 업데이트하는 값을 받아볼 수 있음

# stream()의 updates 모드를 활용해 실행 결과 확인하기
def stream():
    response = graph.stream(
        {
            "messages": ["Langgraph가 무엇인가요?"]
        }
    )
    for chunk in response:
        for node, state in chunk.items():
            print("---", node, "---")
            print(state)
            print("=" * 60)

if __name__ == "__main__":
    stream()
# --- chatbot ---
# {'messages': AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 1194, 'total_tokens': 1211, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_0ae67b3da2', 'id': 'chatcmpl-EVtkWOBCZzcEKCrdxe86nJdwHzBU5', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a11015-07f3-7851-9cc2-ea1b41aaf74b-0', tool_calls=[{'name': 'tavily_search', 'args': {'query': 'Langgraph'}, 'id': 'call_AkkUth8yt4iBYDJteL9gnE0V', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1194, 'output_tokens': 17, 'total_tokens': 1211, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})}
# ============================================================
# --- tools ---
# {'messages': [ToolMessage(content='{"query": "Langgraph", "follow_up_questions": null, "answer": null, "images": [], "results": [{"url": "https://pypi.org/project/langgraph", "title": "LangGraph", "content": "LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. LangGraph provides the infrastructure for", "score": 0.9400512, "raw_content": null, "id": "ed59ca-00"}, {"url": "https://www.geeksforgeeks.org/machine-learning/what-is-langgraph", "title": "What is LangGraph - GeeksforGeeks", "content": "geeksforgeeks\\n\\nsearch icon\\n\\n Courses\\n Interview Prep\\n\\n Python for Machine Learning\\n Machine Learning with R\\n Machine Learning Algorithms\\n EDA\\n Math for Machine Learning\\n Machine Learning Interview Questions\\n ML Projects\\n Deep Learning\\n NLP\\n Computer vision\\n Data Science\\n Artificial Intelligence\\n\\n# What is LangGraph\\n\\nLast Updated : 14 Apr, 2026\\n\\nLangGraph is an open-source framework from LangChain designed to build and manage AI agent workflows using graph-based structures. It allows developers to define workflows as nodes and edges, making complex agent interactions more structured, scalable and easier to control.", "score": 0.9094659, "raw_content": null, "id": "336f15-01"}, {"url": "https://www.ibm.com/think/topics/langgraph", "title": "What is LangGraph? | IBM", "content": "Get hands-on experience with IBM tech Join one of the largest technical IBM community gatherings\\n\\n# What is LangGraph?\\n\\nBy Bryan Clark\\n\\n## LangGraph overview\\n\\nLangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] LangGraph workflow\\n\\n LangGraph workflow\\n\\nLangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\\n\\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences.\\n\\n## LLM integration in LangGraph", "score": 0.90791017, "raw_content": null, "id": "d1fd2b-02"}], "response_time": 0.0, "request_id": "25b14048-6745-4685-bf98-4ce9021e36ad"}', name='tavily_search', id='4897d417-9fa0-49f4-b5a2-99a8a0f4760b', tool_call_id='call_AkkUth8yt4iBYDJteL9gnE0V')]}
# ============================================================
# --- chatbot ---
# {'messages': AIMessage(content='LangGraph는 LangChain에서 개발한 오픈 소스 프레임워크로, 복잡한 AI 에이전트 워크플로우를 구축하고 관리하기 위한 것입니다. 이 프레임워크는 그래프 기반 구조를 사용하여 에이전트의 상호작용을 더 구조화하고 확장 가능하게 만들어 줍니다. LangGraph를 사용하면 개발자는 워크플로우를 노드와 엣지로 정의할 수 있으며, 이것은 복잡한 에이전트 상호작용을 더 잘 통제할 수 있게 해줍니다.\n\n또한, LangGraph는 대규모 언어 모델(LLM)을 작동하고 최적화하는 데 필요한 도구와 라이브러리를 제공하며, 에이전트 시스템을 구축할 수 있는 프레임워크로 사용됩니다. 이러한 구조는 로봇 공학, 자율 주행차, 비디오 게임 같은 다양한 분야에서도 활용될 수 있습니다.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 207, 'prompt_tokens': 1924, 'total_tokens': 2131, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 1152, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_0ae67b3da2', 'id': 'chatcmpl-EVtkYmLfv8vojqeT0F7H0XEAxvkZx', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--01a11015-0eaa-79d2-b23e-d20ea972a594-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 1924, 'output_tokens': 207, 'total_tokens': 2131, 'input_token_details': {'audio': 0, 'cache_read': 1152}, 'output_token_details': {'audio': 0, 'reasoning': 0}})}
# ============================================================

# stream: values 모드 사용하기
# stream()의 values 모드를 활용해 실행 결과 확인하기
def stream_values():
    response = graph.stream(
        {
            "messages": ["Langgraph가 무엇인가요??"]
        },
        stream_mode="values"
    )

    for chunk in response:
        for state_key, state_value in chunk.items():
            print("--- 현재 상태 ---")
            for msg in state_value:
                print(f"{type(msg).__name__}: {msg.content[50:]}")
            if state_key == "messages":
                state_value[-1].pretty_print()
            print("=" * 60)

if __name__ == "__main__":
    stream_values()
# --- 현재 상태 ---
# HumanMessage: 
# ================================ Human Message =================================

# Langgraph가 무엇인가요??
# ============================================================
# --- 현재 상태 ---
# HumanMessage: 
# AIMessage: 
# ================================== Ai Message ==================================
# Tool Calls:
#   tavily_search (call_wH7Bm9mmwgJljouGMJ4PrYeI)
#  Call ID: call_wH7Bm9mmwgJljouGMJ4PrYeI
#   Args:
#     query: Langgraph
# ============================================================
# --- 현재 상태 ---
# HumanMessage: 
# AIMessage: 
# ToolMessage: , "answer": null, "images": [], "results": [{"url": "https://pypi.org/project/langgraph", "title": "LangGraph", "content": "LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. LangGraph provides the infrastructure for", "score": 0.9400512, "raw_content": null, "id": "4d6b26-00"}, {"url": "https://www.geeksforgeeks.org/machine-learning/what-is-langgraph", "title": "What is LangGraph - GeeksforGeeks", "content": "geeksforgeeks\n\nsearch icon\n\n Courses\n Interview Prep\n\n Python for Machine Learning\n Machine Learning with R\n Machine Learning Algorithms\n EDA\n Math for Machine Learning\n Machine Learning Interview Questions\n ML Projects\n Deep Learning\n NLP\n Computer vision\n Data Science\n Artificial Intelligence\n\n# What is LangGraph\n\nLast Updated : 14 Apr, 2026\n\nLangGraph is an open-source framework from LangChain designed to build and manage AI agent workflows using graph-based structures. It allows developers to define workflows as nodes and edges, making complex agent interactions more structured, scalable and easier to control.", "score": 0.9094659, "raw_content": null, "id": "6da9cc-01"}, {"url": "https://www.ibm.com/think/topics/langgraph", "title": "What is LangGraph? | IBM", "content": "Get hands-on experience with IBM tech Join one of the largest technical IBM community gatherings\n\n# What is LangGraph?\n\nBy Bryan Clark\n\n## LangGraph overview\n\nLangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] LangGraph workflow\n\n LangGraph workflow\n\nLangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\n\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences.\n\n## LLM integration in LangGraph", "score": 0.90791017, "raw_content": null, "id": "6c410e-02"}], "response_time": 0.0, "request_id": "80e41f32-30bf-4a24-aa93-cc560a84b49a"}
# ================================= Tool Message =================================
# Name: tavily_search

# {"query": "Langgraph", "follow_up_questions": null, "answer": null, "images": [], "results": [{"url": "https://pypi.org/project/langgraph", "title": "LangGraph", "content": "LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. LangGraph provides the infrastructure for", "score": 0.9400512, "raw_content": null, "id": "4d6b26-00"}, {"url": "https://www.geeksforgeeks.org/machine-learning/what-is-langgraph", "title": "What is LangGraph - GeeksforGeeks", "content": "geeksforgeeks\n\nsearch icon\n\n Courses\n Interview Prep\n\n Python for Machine Learning\n Machine Learning with R\n Machine Learning Algorithms\n EDA\n Math for Machine Learning\n Machine Learning Interview Questions\n ML Projects\n Deep Learning\n NLP\n Computer vision\n Data Science\n Artificial Intelligence\n\n# What is LangGraph\n\nLast Updated : 14 Apr, 2026\n\nLangGraph is an open-source framework from LangChain designed to build and manage AI agent workflows using graph-based structures. It allows developers to define workflows as nodes and edges, making complex agent interactions more structured, scalable and easier to control.", "score": 0.9094659, "raw_content": null, "id": "6da9cc-01"}, {"url": "https://www.ibm.com/think/topics/langgraph", "title": "What is LangGraph? | IBM", "content": "Get hands-on experience with IBM tech Join one of the largest technical IBM community gatherings\n\n# What is LangGraph?\n\nBy Bryan Clark\n\n## LangGraph overview\n\nLangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] LangGraph workflow\n\n LangGraph workflow\n\nLangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\n\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences.\n\n## LLM integration in LangGraph", "score": 0.90791017, "raw_content": null, "id": "6c410e-02"}], "response_time": 0.0, "request_id": "80e41f32-30bf-4a24-aa93-cc560a84b49a"}
# ============================================================
# --- 현재 상태 ---
# HumanMessage: 
# AIMessage: 
# ToolMessage: , "answer": null, "images": [], "results": [{"url": "https://pypi.org/project/langgraph", "title": "LangGraph", "content": "LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. LangGraph provides the infrastructure for", "score": 0.9400512, "raw_content": null, "id": "4d6b26-00"}, {"url": "https://www.geeksforgeeks.org/machine-learning/what-is-langgraph", "title": "What is LangGraph - GeeksforGeeks", "content": "geeksforgeeks\n\nsearch icon\n\n Courses\n Interview Prep\n\n Python for Machine Learning\n Machine Learning with R\n Machine Learning Algorithms\n EDA\n Math for Machine Learning\n Machine Learning Interview Questions\n ML Projects\n Deep Learning\n NLP\n Computer vision\n Data Science\n Artificial Intelligence\n\n# What is LangGraph\n\nLast Updated : 14 Apr, 2026\n\nLangGraph is an open-source framework from LangChain designed to build and manage AI agent workflows using graph-based structures. It allows developers to define workflows as nodes and edges, making complex agent interactions more structured, scalable and easier to control.", "score": 0.9094659, "raw_content": null, "id": "6da9cc-01"}, {"url": "https://www.ibm.com/think/topics/langgraph", "title": "What is LangGraph? | IBM", "content": "Get hands-on experience with IBM tech Join one of the largest technical IBM community gatherings\n\n# What is LangGraph?\n\nBy Bryan Clark\n\n## LangGraph overview\n\nLangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] LangGraph workflow\n\n LangGraph workflow\n\nLangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\n\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences.\n\n## LLM integration in LangGraph", "score": 0.90791017, "raw_content": null, "id": "6c410e-02"}], "response_time": 0.0, "request_id": "80e41f32-30bf-4a24-aa93-cc560a84b49a"}
# AIMessage: 복잡한 생성적 AI 에이전트 워크플로우를 구축, 배포 및 관리할 수 있도록 설계되었습니다. 이 프레임워크는 그래프 기반의 구조를 활용하여 에이전트 워크플로우 내의 다양한 구성 요소 간의 복잡한 관계를 모델링하고 관리할 수 있습니다.

# 주요 기능으로는 AI 에이전트 워크플로우의 상태를 추적하고 기록하는 기능이 있으며, 이는 시스템이 다양한 워크플로우 단계를 거치면서 처리한 모든 중요한 정보를 기록하고 업데이트합니다. 이를 통해 LangGraph는 보다 구조적이고 확장 가능하며 관리하기 쉬운 복잡한 에이전트 상호작용을 지원합니다. 이 프레임워크는 로봇공학, 자율 주행차, 비디오 게임과 같은 에이전트 기반 시스템을 구축하는 데 사용할 수 있습니다.

# 자세한 정보는 [여기](https://pypi.org/project/langgraph)에서 확인할 수 있습니다.
# ================================== Ai Message ==================================

# LangGraph는 LangChain에서 만든 오픈 소스 AI 에이전트 프레임워크입니다. 복잡한 생성적 AI 에이전트 워크플로우를 구축, 배포 및 관리할 수 있도록 설계되었습니다. 이 프레임워크는 그래프 기반의 구조를 활용하여 에이전트 워크플로우 내의 다양한 구성 요소 간의 복잡한 관계를 모델링하고 관리할 수 있습니다.

# 주요 기능으로는 AI 에이전트 워크플로우의 상태를 추적하고 기록하는 기능이 있으며, 이는 시스템이 다양한 워크플로우 단계를 거치면서 처리한 모든 중요한 정보를 기록하고 업데이트합니다. 이를 통해 LangGraph는 보다 구조적이고 확장 가능하며 관리하기 쉬운 복잡한 에이전트 상호작용을 지원합니다. 이 프레임워크는 로봇공학, 자율 주행차, 비디오 게임과 같은 에이전트 기반 시스템을 구축하는 데 사용할 수 있습니다.

# 자세한 정보는 [여기](https://pypi.org/project/langgraph)에서 확인할 수 있습니다.
# ============================================================

# stream: messages 모드 사용하기
# messages 모드는 각 단게에서 생성되는 메시지 상태만 스트리밍 방식으로 출력
# 이 모드를 사용하면 LLM의 응답 결과로 출력되는 텍스트가 완성된 문장 단위가 아닌, 토큰 단위로 순차적으로 전달
# 응답이 모두 생성된 후 한 번에 출력되는 것이 아니라, 텍스트가 실시간으로 생성되는 즉시 화면에 점진적으로 표시
# 사용자가 다변을 기다리는 동안 진행 상황을 확인할 수 있게 해주어 챗봇의 응답 속도가 더 빠르게 느껴지도록 함
# 실제 서비스 환경에서 보다 자연스러운 대화 경험을 제공하는 데 유용

# stream()의 messages 모드를 활용해 실행 결과 확인하기
def stream_messages():
    response = graph.stream(
        {
            "messages": ["Langgraph가 무엇인가요?"]
        },
        stream_mode="messages"
    )

    for token, metadata in response:
        print(token.content)
        # print(metadata["langraph_node"])

if __name__ == "__main__":
    stream_messages()

# {"query": "Langgraph", "follow_up_questions": null, "answer": null, "images": [], "results": [{"url": "https://pypi.org/project/langgraph", "title": "LangGraph", "content": "LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. LangGraph provides the infrastructure for", "score": 0.9400512, "raw_content": null, "id": "10aeb1-00"}, {"url": "https://www.geeksforgeeks.org/machine-learning/what-is-langgraph", "title": "What is LangGraph - GeeksforGeeks", "content": "geeksforgeeks\n\nsearch icon\n\n Courses\n Interview Prep\n\n Python for Machine Learning\n Machine Learning with R\n Machine Learning Algorithms\n EDA\n Math for Machine Learning\n Machine Learning Interview Questions\n ML Projects\n Deep Learning\n NLP\n Computer vision\n Data Science\n Artificial Intelligence\n\n# What is LangGraph\n\nLast Updated : 14 Apr, 2026\n\nLangGraph is an open-source framework from LangChain designed to build and manage AI agent workflows using graph-based structures. It allows developers to define workflows as nodes and edges, making complex agent interactions more structured, scalable and easier to control.", "score": 0.9094659, "raw_content": null, "id": "0a6635-01"}, {"url": "https://www.ibm.com/think/topics/langgraph", "title": "What is LangGraph? | IBM", "content": "Get hands-on experience with IBM tech Join one of the largest technical IBM community gatherings\n\n# What is LangGraph?\n\nBy Bryan Clark\n\n## LangGraph overview\n\nLangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] LangGraph workflow\n\n LangGraph workflow\n\nLangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\n\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences.\n\n## LLM integration in LangGraph", "score": 0.90791017, "raw_content": null, "id": "d6990b-02"}], "response_time": 0.01, "request_id": "ffb7690f-46fd-4af5-83c4-82d692a271b6"}

# Lang
# Graph
# 는
#  Lang
# Chain
# 에서
#  개발
# 한
# ...(중략)...
# 될
#  수
#  있습니다
# .

# 앞에서 확인한 모든 스트리밍 방식은 비동기 방시으로 처리될 수 있음. 이때는 astream 메서드를 통해 구현 가능
# astream()를 활용해 실행 결과 확인하기
async def astream():
    response = graph.astream(
        {
            "messages": ["Langgraph가 무엇인가요?"]
        }
    )
    async for chunk in response:
        for node, state in chunk.items():
            print("---", node, "---")
            print(state)
            print("=" * 60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(astream())

# ------------------------------------

# 사용자 도구 정의하기
# 도구의 설명을 docstring에서 추출하기
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

print(multiply.name)
print(multiply.description)
print(multiply.args)