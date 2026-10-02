# 그래프의 실행 경로, 엣지 추가하기
# 엣지 (edge)는 다음에 실행될 경로를 결정
# 특히 에이전트 시스템에서 다음 작업을 결정하는 데 꼭 필요한 요소
# 반드시 시작점(START)과 종료(END)점이 존재
# 시스템 내에 정의되어야 할 노드(node)가 1개더라도 시작점 - 노드 - 종료점을 연결해야 함
# 이때 총 2개의 엣지가 연결되어야 함

# --------------------------------------

# 시작점과 종료점 엣지 연결하기
from langgraph.graph import START, END

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)