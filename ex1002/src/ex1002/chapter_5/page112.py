# 03 에이전트 조건부 엣지 설정하기
# 사용자 입력의 길이가 너무 짧을 경우 답변하지 않는 챗봇을 만들고자 함
# 따라서 사용자 입력이 일정 길이 이상일 겨우에만 chatbot 노드에 들어올 수 있도록 조건부 엣지를 설정
# 조건부 엣지를 설정하는 add_conditional_edges 메서드의 파라미터 중, 라우팅 조건을 정의하는 함수인 routing_function을 살펴보겠음
# 해당 엣지가 실행되는 시점은 guardrail 노드가 실행된 이후이므로 사용자의 입력 길이인 "question_length"가 저장되어 있을 것
# 이때 이 값이 3을 초과하는 경우에만 "chatbot" 노드로 보내지도록 설정
# 즉, 사용자의 입력이 세 글자 이하라면 오타이거나 질문의 형태가 아니라고 판단해 종료

# 라우팅 함수 정의하고 조건부 엣지 추가하기
def routing_function(state: State) -> str:
    if state["question_length"] > 3:
        return "chatbot"
    else: 
        return END

graph_builder.add_conitional_edges(
    "guardrail",
    routing_function,
    {"chatbot": "chatbot", END: END}
)
# 남은 엣지를 연결해주고 모든 노드와 엣지가 추가된 그래프에 컴파일하면 완료

# 엣지 연결하고 그래프 컴파일하기
graph_builder.add_edge(START, "guardrail")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()