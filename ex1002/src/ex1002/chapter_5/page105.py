# 5.3 랭그래프로 에이전트 설계하고 구현하기
# 챗봇을 위한 그래프
# 구현 과정에서 챗봇의 기능이 어떻게 구축되어 가는지, 그 흐름을 중심으로 살펴보는 것이 좋음

# 5.3.1 답변을 생성하는 기본 그래프 구현하기
# 01. 그래프 상태 정의 및 상태그래프 생성하기
# 먼저 챗봇 시스템에서 기본적으로 관리해야 하는 상태를 정의
# 메시지를 기반으로 동작하는 시스템이니 메시지를 관리하는 키가 있으면 좋음
# 사용자의 입력은 question, AI가 생성한 답변은 answer 키로 구분하여 관리
# 이때 그래프의 입력과 출력에 서로 다른 스키마(schema)를 사용할 수 있는데, 그래프의 입력 스키마와 출력 스키마를 다르게 정의한다는 것은 입력과 출력에 필요한 최소한의 키만 정의할 수 있다는 뜻
# 입력과 출력에 다른 스키마를 적용할 수 있으며, 그래프의 전체 상태(overall state)는 입력과 출력 상태에 포함된 키 외에는 다른 키도 포함할 수 있음
# 서로 다른 상태를 정의하기 위해 총 3개의 클래스를 구현
# InputState: question 키만 사요하여 문자열 타입을 입력받을 수 있도록
# OutputState: answer 키를 사용해 문자열 타입의 출력을 반환할 수 있도록
# OverallState: messages, question, answer 총 세 가지 키를 포함

# ------------------------------------------------------

# 그래프의 입력 스키마와 출력 스키마 정의
class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(TypedDict):
    messages: Annotated[list[str], add]
    question: str
    answer: str

# ------------------------------------------------------

# 이 상태 기반의 그래프를 구축
# 그래프의 노드와 엣지를 추가하기 전에 StateGraph를 통해 그래프 객체를 새성
# StateGraph의 첫 번째 파라미터인 state_schema에는 그래프 전반에서 공유되는 상태 구조를 정의한 OverallState를 전달하고, Input_schema와 output_schema 파라미터를 통해 앞서 정의한 입력 스키마와 출력 스키마를 각각 전달

# 그래프 객체 생성하기
from langgraph.graph import StateGraph

graph_builder = StateGraph(
    OverallState,
    input_schema=InputState,
    output_schema=OutputState
)

# 상태 그래프(StateGraph)는 사태를 읽고 쓰는 방식으로 통신하는 그래프
# 이 상태그래프로 그래프 내에서 사용할 사태를 정의하고 노드와 엣지를 추가
# 노드와 엣지를 추가하기 위해 사용했던 add_node, add_edge, add_conditional_edges는 모두 StateGraph의 메서드
# 상태가 정의된 그래프에 노드와 엣지를 추가하게 됨