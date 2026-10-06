# 04 그래프 실행하기
# 컴파일된 그래프를 통해 답변을 얻음
# 그래프의 입력 상태는 InpuState로, "question" 키에 질문을 담아 입력
# 이때 그래프에 입력을 전달하여 실행하기 위해 invoke 메서드를 사용
# invoke는 하나의 요청에 대한 결과를 받기 위해 전체 그래프를 한 번에 실행하는 방식으로, 한 번에 하나의 요청만 처리
# 이를 통해 그래프의 최종 출력을 확인
# 그래프 겨로가 호출 방식은 invoke 외에도 다양함
# 그래프의 출력을 보니 출력 상태로 정의했던 OutputState의 "answer" 키만 반환되는 것을 확인

# ------------------------------------

# 'question' 키에 질문을 담아 그래프 실행하기
graph.invoke({"question": "What is the capital city of South Korea?"})