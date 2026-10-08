from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

# 1. 간단한 State 정의
class SimpleState(TypedDict):
    text: str

# 2. 노드 함수 정의
def step_1(state: SimpleState):
    return {"text": state["text"] + " -> Step 1"}

def step_2(state: SimpleState):
    return {"text": state["text"] + " -> Step 2"}

# 3. 그래프 생성 및 연결
builder = StateGraph(SimpleState)

builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", END)

# 4. 그래프 컴파일
graph = builder.compile()

# ==========================================
# 5. 그래프 시각화 방법
# ==========================================

# 방법 D: LangSmith Studio -> 터미널에서 `uv run langgraph dev` 실행
# (langgraph.json 이 위의 `graph` 변수를 가리킴)

# 직접 실행(python langgraphtest.py)할 때만 동작. Studio 서버가 import 할 때는 건너뜀
if __name__ == "__main__":
    # 방법 A: 터미널/콘솔용 ASCII 텍스트 아트 출력
    print(graph.get_graph().draw_ascii())

    # 방법 B: PNG 이미지 파일로 저장
    try:
        png_bytes = graph.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_bytes)
        print("graph.png 파일로 저장되었습니다.")
    except Exception as e:
        print(f"이미지 생성 실패 (Graphviz 필요): {e}")

    # 방법 C: Jupyter Notebook 환경에서 바로 출력
    # from IPython.display import Image, display
    # display(Image(graph.get_graph().draw_mermaid_png()))