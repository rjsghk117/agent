# 04 에이전트 그래프 시각화 및 실행
# 컴파일된 그래프를 시각화
# 가장 먼저 사용자의 입력이 guardrail 노드로 전달되어 입력 길이르 저장
# 이후 조건부 엣지에 따라 길이가 3 이하이면 바로 종료, 3을 초과하면 chatbot 노드를 실행해 답변을 생성한 뒤 종료

# 그래프 시각화
from IPython import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass
# 이제 invoke를 통해 입력
# "messages"에 "ㅇ"만 입력하니 guardrail 노드 이후 조건부 엣지에 의해 바로 종료
graph.invoke({"messages":["ㅇ"]})

# 그러나 "안녕하세요"와 같이 세 글자 이상 입력하니, AI가 생성한 답변이 "messages"에 저장되어 반환
graph.invoke({"messages": ["안녕하세요"]})