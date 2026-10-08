# response_format 기반 구조화 응답 출력하기
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.tools import tool

class ContactInfo(BaseModel):
    """연락처 정보 스키마"""
    name: str = Field(description="이름")
    email: str = Field(description="이메일 주소")
    phone: str = Field(description="전화번호")

model = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(
    model=model,
    tools=[...],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "다음 텍스트에서 연락처 정보를 추출해줘: John Doe, john@example.com, (555) 123-4567"
    }]
})

contact = result["structured_response"]
print(f"이름: {contact.name}")
print(f"이메일: {contact.email}")
print(f"전화번호: {contact.phone}")

