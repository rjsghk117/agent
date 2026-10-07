# 01 코드를 실행하는 도구 생성
# 에이전트가 코딩을 수행할 수 있도록, 생성된 코드를 실행하는 도구를 만듦
# 코드 실행 시 오류가 발생하는지 확인하는 용도로 사용

# 코드 실행하는 도구 만들기
from pydantic import Field
from langchain.tools import tool

@tool
def python_exec_tool(
    imports: str = Field(description="임포트 구문"), # ----------- [ 1 ]
    code: str = Field(description="임포트 구문을 제외한 코드 블록")
) -> str:
    """
    파이썬 코드를 실행하는 도구입니다. 만약 코드 실행에 실패하면 에러 메시지를 반환합니다.
    실행 결과를 확인하고 싶다면 'print(...)'를 사용하여 출력해야 합니다.
    
    Args:
        import: 임포트 구문
        code: 임포트 구문을 제외한 코드 블록
        
    Returns:
        실행 결과 또는 에러 메시지
    """
    # Check imports
    try:
        exec(imports)
    except Exception as e:
        return f"모듈을 임포트하는데 실패했습니다. ERROR: {repr(e)}"

    # Check execution
    try:
        exec(imports + "\n" + code)
    except Exception as e:
        return f"코드 실행에 실패했습니다. ERROR: {repr(e)}"

    result_str = f"성공적으로 코드가 실행되었습니다. :\n'''python\n{code}\n'''"

    return result_str

# --------------------------------

# create_agent 기반 에이전트 구축
# 파이썬 코딩 도구를 사용하는 에이전트를 만들어보자
# Langchain에서 제공하는 표준 에이전트 생성 함수인 create_agent를 활용하면 도구를 사용하는 에이전트를 간단하게 생성 가능
# create_agent는 두 가지 필수 파라미터만 전달하면 도구 호출을 기반으로 동작하는 에이전트를 생성 가능
# - model: 에이전트가 사용할 LLM
# - tools: 에이전트가 사용할 도구의 목록

# create_agent를 사용하여 에이전트 만들기
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

tools = [python_exec_tool]

llm = ChatOpenAI(model="gpt-4o")
graph = create_agent(llm, tools)

# 에이전트 답변 확인하기
# stream 메서드를 활용해 그래프의 답변을 확인
# 코드를 생성하고 실행하는 도구를 사용할 수 있도록 피보나치 수열을 출력하는 파이썬 코드를 작성하도록 요청

# 피보나치 수열 코드 작성 요청
if __name__ == "__main__":
    response = graph.stream(
        {
            "messages": [
                "첫 번째 항이 1인 피보나치 수열을 출력하는 파이썬 코드를 작성해주세요."
            ]
        }
    )

    for chunk in response:
        for node, value in chunk.items():
            if node:
                print("---", node, "---")
            if "messages" in value:
                print(value['messages'][0].content)

# ----- RESULT -----

# --- model ---
# 피보나치 수열은 각 항이 바로 앞의 두 항의 합으로 이루어진 수열입니다. 첫 번째 항이 1인 피보나치 수열을 출력하는 파이썬 코드는 다음과 같습니다.

# ```python
# def fibonacci_sequence(n):
#     sequence = [1, 1]
#     while len(sequence) < n:
#         next_value = sequence[-1] + sequence[-2]
#         sequence.append(next_value)
#     return sequence

# # 첫 번째 항이 1인 피보나치 수열을 10개 항까지 출력
# fib_sequence = fibonacci_sequence(10)
# print(fib_sequence)
# ```

# 위 코드는 첫 번째 항과 두 번째 항을 모두 1로 시작합니다. 그런 다음 루프를 사용하여 n개의 항으로 구성된 피보나치 수열을 생성합니다. 이 예제에서는 10개의 항을 생성합니다. 필요에 따라 `fibonacci_sequence(10)`의 인자를 변경하여 원하는 길이의 피보나치 수열을 생성할 수 있습니다.

# 파일을 저장하는 도구 만들기
@tool
def file_write_tool(
    file_path: str = Field(description="생성/수정할 파일의 경로"),
    content: str = Field(description="파일에 작성할 내용")
) -> str:
    """
    파일을 생성하거나 내용을 작성하는 도구입니다.
    
    Args:
        file_path: 생성/수정할 파일의 경로
        content: 파일에 작성할 내용
        
    Returns:
        성공/실패 메시지
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"파일 '{file_path}'에 성공적으로 작성했습니다."
    except Exception as e:
        return f"파일 자성 실패: {repr(e)}"

# 두 가지 도구 기반 에이전트 생성하기
# 코드 실행 도구와 더불어 파일 저장 도구도 함께 사용하는 ReAct 패턴 에이전트를 직접 만들어본다

tools = [python_exec_tool, file_write_tool]

llm = ChatOpenAI(model="gpt-4o")
graph = create_agent(llm, tools)

# 에이전트 답변 확인하기
# 코드를 작성하고 파일로 저장하는 요청하기

if __name__ == "__main__":
    response = graph.stream(
        {
            "messages": [
                "첫 번째 항이 1이 피보나치 수열을 출력하는 파이썬 코드를 작성해주세요. 정상적으로 실행되는지 확인도 해주세요.",
                "확인했다면 그 코드는 .py 파일로 저장하세요."
            ]
        }
    )

    for chunk in response:
        for node, value in chunk.items():
            if node:
                print("---", node, "---")
            if "messages" in value:
                print(value['messages'][0].content)

# ----- RESULT -----
# --- model ---

# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
# --- tools ---
# 성공적으로 코드가 실행되었습니다. :
# '''python
# def fibonacci_sequence(n):
#     fib_sequence = [1, 1]
#     while len(fib_sequence) < n:
#         next_value = fib_sequence[-1] + fib_sequence[-2]
#         fib_sequence.append(next_value)
#     return fib_sequence

# # 피보나치 수열의 처음 10개 항 출력
# print(fibonacci_sequence(10))
# '''
# --- model ---

# --- tools ---
# 파일 'fibonacci_sequence.py'에 성공적으로 작성했습니다.
# --- model ---
# 첫 번째 항이 1인 피보나치 수열을 출력하는 파이썬 코드를 작성하고, 이를 `fibonacci_sequence.py`라는 파일에 저장했습니다. 코드도 성공적으로 실행되었습니다.

# -------------------------------------------------------

# 주요 파라미터 이해하기
# create_agent 주요 파라미터 살펴보기
# create_agent(
#     model: str | BaseChatModel,
#     tools: Sequence[BaseTool | Callable | dict[str, Any]] | None = None,
#     *,
#     system_prompt: str | SystemMessage | None = None,
#     middleware: Sequence[AgentMiddleware[StateT_co, ContextT]] = (),
#     response_format: ResponseFormat[ResponseT] | type[ResponseT] | None = None,
#     state_schema: type[AgentState[ResponseT]] | None = None,
#     context_schema: type[ContextT] | None = None,
#     checkpointer: Chekpointer | None = None,
#     store: BaseStore | None = None,
#     interrupt_before: list[str] | None = None,
#     interrupt_after: list[str] | None = None,
#     debug: bool = False,
#     name: str | None = None,
#     cache: BaseCache | None = None,
# ) -> CompiledStateGraph[
#     AgentState[ResponseT], ContextT, _InputAgentState, _OutputAgentState[ResponseT]
# ]

# ----------------------------------------------

# 커스텀 state 스키마 정의하기
# from langchain.agents import AgentState

# class CustomState(AgentState):
#     user_preferences: dict

# agent = create_agent(
#     model,
#     tools=[tool1, tool2],
#     state_schema=CustomState
# )