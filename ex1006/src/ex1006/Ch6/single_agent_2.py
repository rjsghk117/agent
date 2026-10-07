# 전달인자(argument) 스키마
# 데코레이터의 args_schema 속성을 사용하여 정의 할 수 있음
# 곱셈 도구의 입력인자를 사전에 정의한 스키마로 전달하는 예시

# CalculatorInput라는 클래스를 정의하여 각 인자의 데이터 타입과 설명을 지정할 수 있음.
# 이 클래스는 pydantic.BaseModel을 상속받아 필드와 설명을 명확히 선언
# 이후 @tool(args_schema=CalculatorInput)으로 데코레이터를 적용하면 해당 스키마가 도구 입력으로 사용됨

# 도구의 전달인자 스키마를 정의하기
from pydantic import BaseModel, Field
from langchain.tools import tool

class CalculatorInput(BaseModel):
    a : int = Field(description="first number")
    b : int = Field(description="second number")

@tool(args_schema=CalculatorInput)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# print(multiply.name)
# print(multiply.description)
# print(multiply.args)

# ----- RESULT -----
# multiply                                                                                                                                                                                          
# Multiply two numbers.                                                                                                                                                                             
# {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}   

# Google 스타일의 독스트링 작성하기
@tool(parse_docstring=True)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.
    
    Args:
        a: The first number.
        b: The second number.
    """
    return a * b

# print(multiply.name)
# print(multiply.description)
# print(multiply.args)

# ----- RESULT -----
# multiply                                                                                                                                                                                          
# Multiply two numbers.                                                                                                                                                                             
# {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}  

# json 형식으로 파싱하여 확인도 가능
# print(multiply.args_schema.model_json_schema())

# ----- RESULT -----
# {'description': 'Multiply two numbers.', 'properties': {'a': {'description': 'The first number.', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'The second number.', 'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'multiply', 'type': 'object'}   

