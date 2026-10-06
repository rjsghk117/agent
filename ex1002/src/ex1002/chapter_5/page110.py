# 5.3.2 조건이 추가된 그래프 구현하기
# 이번에는 사용자의 입력을 받아와 사용자의 입력이 너무 짧으면 종료하고, 특정 길이 이상일 때만 chatbot 노드로 보내주는 에이전트를 만들기

# ------------------------------------------------

# 01 에이전트 상태 정의 및 상태 그래프 생성하기
# 먼저 상태를 정의
# 이번에는 입력과 출력 그리고 내부 모두 동일한 상태를 갖게 하고, 메시지 관리를 위한 "messages" 키, 질문의 길이를 저장하기 위한 "question_length" 키를 가지는 상태를 만들기
# "messages" 키에는 새로운 메시지들이 모두 저장될 수 있도록 add 리듀서 함수를 지정했고, "question_length" 키에는 질문의 길이가 정수로 저장되도록 데이터 타입을 지정

# 그래프 상태 정의하기
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list[str], add]
    question_length: int

    # 이 State 기반 그래프는 StateGraph를 통해 상태그래프 객체를 생성

# 상태그래프 생성하기
from langgraph.graph import StateGraph

graph_builder = StateGraph(State)