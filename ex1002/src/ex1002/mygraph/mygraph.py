from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()
# Mermaid로 그렸음
print(graph.get_graph().draw_mermaid())

# 실행
result = graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})

# ---------------------------------
# 결과
print(result)
print(f"AIMessage: {result["messages"][-1].content}")
