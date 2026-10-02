# 02 그래프 노드 생성하기
# 상태와 초기 그래프를 생성해주었으니 이제 챗봇의 작업을 수행할 노드를 만듦
# 입력 메시지를 받아 LLM을 통해 답변을 새성하는 노드를 구현
# 노드 구현을 위해 노드가 입력받을 값과 처리된 값을 상태의 어떤 키로 업데이트할지 생각해야 함
# 사용자 질문은 question 키를 포함한 입력 상태로 전달
# chatbot 노드는 이 질문에 대한 답변을 처리하고 그 결과를 answer에 저장하며 지금까지 업데이트된 메시지 또한 messages 키에 저장하도록 구현
# question -> chatbot -> answer messages

# ---------------------------------------------

# chatbot 노드 함수의 내부
# chatbot 노드는 InputState를 입력으로 받음
# InputState에는 question 키를 가지고 있고, 이 키에는 사용자의 질문이 입력되어 넘어왔을 것
# 해당 키의 값을 question 변수로 저장해 LLM이 입력으로 전달
# LLM 답변 결과는 response 변수에 담겨 저장

# --------------------------------------------

# 노드의 반환값
# 노드의 반환값은 그래프의 상태 업데이트를 해주는 역할
# 해당 노드의 반환값은 딕셔너리 형태이고 answer 키와 messages 키를 가지고 있음
# OverallState의 두 가지 키를 업데이트하겠다는 의미
# "answer"에는 LLM이 생성한 답변 문자열을 업데이트하고, "messages"에는 사용자의 질문과 LLM의 답변을 순서대로 문자열에 담아 업데이트
# 마지막으로 add_node를 통해 구현한 함수를 전달하여 "chatbot"이라는 이름을 가진 노드를 추가

# --------------------------------------------

# LLM의 답변을 생성하는 노드 추가하기
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def chatbot(state: InputState) -> OverallState:
    question = state["question"]
    response = llm.invoke(question)
    return(
        "answer":response.content,
        "messages": [question, response.content]
    )

graph_builder.add_node("chatbot", chatbot)