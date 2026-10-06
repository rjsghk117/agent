# 02 에이전트 노드 생성하기
# 정의한 State를 가지는 상태 그래프를 생성했음
# 이제 이 graph_builder에 노드와 엣지를 추가하며 그래프를 구축
# 먼저, 사용자 질문을 받아 그 질문의 길이를 question_length에 저장하는 노드를 생성
# 해당 노드에서는 messages 키에 있는 메시지 중 가장 최신의 것, 즉 사용자의 입려을 받아옴
# 그리고 그 입력 길이를 "question_length"키에 업데이트

# -----------------------------------

# 질문의 길이를 저장하는 노드 만들기
def guardrail(state: State) -> State:
    question_length = len(state["messages"][-1])
    return {
        "question_length": question_length
    }

graph_builder.add_node("guardrail", guardrail)
# TIP: guardrail는 첫 번째 노드이므로 messages 리스트에 첫 번째 메시지 하나만 들어 있을 것
# 따라서 입력 메시지는 messages 키의 인덱스 0의 값(state["messages"][0])을 사용해도 무방

# --------------------------------------

# 다음은 사용자 입력에 대한 답변을 생성하는 노드
# 상태의 "messages" 리스트에서 사용자 입력을 받아와 question으로 저장하고, 이 question을 LLM에 전달하여 생성된 답변을 받아 response에 저장
# 그리고 "messages" 키에 새롭게 생성된 답변을 리스트 형태로 전달해 업데이트

# 질문에 대한 답변을 생성하는 노드 만들기
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def chatbot(state:State) -> State:
    question = state["messages"][-1]
    response = llm.invoke(question)
    return {
        "messages": [response.content]
    }

graph_builder.add_node("chatbot", chatbot)