# 03 그래프 엣지 생성 및 그래프 컴파일하기
# 이제 엣지를 연결할 차례
# 하나의 노드에 답변만 수행하는 단순한 그래프이므로, chatbot 노드의 앞뒤에 시작점과 종료점만 연결해주면 됨
# 연결했다면 compile() 메서드를 통해 StateGraph였던 그래프를 실행 가능한 형태인 CompileStateGraph로 변환해주면 끝

# ----------------------------------------------

# Chatbot 노드에 엣지를 연결하고 컴파일하기
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# 그래프 시각화하기
from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass