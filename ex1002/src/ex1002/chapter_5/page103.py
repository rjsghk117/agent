# 그래프에 조건부 엣지 추가하기
# 에이전트 시스템을 설계하다 보면 조건에 따라 경로를 다르게 구성해야 하는 상황을 마주하게 된다
# 라우터 LLM에서의 결정에 따라 다음 단계가 달라지는 경우, 조건부 엣지(conditional edge)를 통해 조건에 따라 달라지는 경로를 구현

# -------------------------------------------

# 라우팅 함수 정의하고 조건부 엣지 추가하기
def routing_function(state: State):
    if len(state["messages"][-1]) > 1000 :
        return True
    return False

graph.add_conditional_edges(
    "chatbot",
    routing_function,
    {True: "summary", False: END}
)

# 조건부 엣지를 사용하면 에이전트의 실행 흐름을 상태와 조건에 따라 유연하게 제어할 수 있다
# 특히, 응답 길이, 의도 분류 결과 등 라우터 역할을 하는 중간 노드의 출력 결과를 기준으로 다음 행동을 결정해야 하는 경우에 사용
