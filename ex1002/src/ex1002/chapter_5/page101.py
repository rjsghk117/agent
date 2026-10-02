# 그래프 상태에 답변 결과를 반환하기
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import START, END

from langgraph.graph import StateGraph

class State(TypedDict):
    messages: Annotated[list[str], add]

graph = StateGraph(State)
def chatbot(state: State):
    question = state["messages"]
    answer = f"사용자 입력을 그대로 반환하는 챗봇입니다. {question}라는 질문을 받았습니다."
    return {"messages": [answer]}

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()

result = app.invoke({"messages": ["안녕"]})
print(result)