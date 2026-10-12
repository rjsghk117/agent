# RAG를 위한 에이전트 만들기
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
import asyncio

load_dotenv()

file_path = "src/ex1006/Ch6/법률(2007).pdf"

loader = PyPDFLoader(file_path)
pages = []

async def load_pages():
    async for page in loader.alazy_load():
        pages.append(page)


asyncio.run(load_pages())

print("페이지 수:", len(pages))
print("첫 번째 페이지 정보:", pages[0])

# 페이지 수: 161
# 첫 번째 페이지 정보: page_content='' metadata={'producer': 'PyPDF', 'creator': 'PyPDF', 'creationdate': '2014-10-02T16:51:33+09:00', 'moddate': '2014-10-02T16:51:33+09:00', 'source': 'src/ex1006/Ch6/법률(2007).pdf', 'total_pages': 161, 'page': 0, 'page_label': '1'}

# 텍스트 분할하기
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(pages)

# 청크 정보 확인하기
print(f"총 {len(docs)}개의 청크 생성 완료")
print("각 청크의 길이:", [len(i.page_content) for i in docs])

for i in docs:
    print("[메타데이터]", i.metadata)
    print("[내용]", i.page_content)
    print("=" * 100)
# 총 0개의 청크 생성 완료
# 각 청크의 길이: []
# pdf가 스캔본 + 투명 글자층 형태

# ----------------------------------------------

# 벡터 스토어 생성하기
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

DB_PATH = "./chroma_db"

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory=DB_PATH,
    vectorstore.similarity_search("...", k=3)
)

# 벡터 스토어에서 유사도 검색을 하는 리트리버 도구 만들기
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import create_retriever_tool
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "..."

vectorstore = Chroma(
    persist_directory=DB_PATH,
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="korean_pdf"
)
vectorstore.get()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

retriever_tool = create_retriever_tool(
    retriever,
    name="pdf_search",
    description="use this tool to search information from the Korean Spelling Rules PDF document"
)

# RAG를 위한 상태 정의하기
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    question: str
    context: str
    answer: str
    retry_num: int

# 검색 도구를 호추하는 LLM 노드 만들기
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage
from langchain_core.messages import AIMessage

from retriever import retriever, retriever_tool
from state import AgentState

llm = ChatOpenAI(model="gpt-4o")

def chatbot(state: AgentState):
    """
    검색(Retriever) 도구를 바인딩한 LLM 모델에 현재 메시지 상태를 입력하여 응답을 생성합니다.
    질문이 주어지면 검색 도구를 도구 호출하거나 일반 답변하며 종료할지 결정할 수 있습니다.
    """
    print("----- [CHATBOT] -----")
    messages = state["messages"]
    llm_with_tools = llm.bind_tools([retriever_tool])
    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response],
        "question": messages[-1].content
    }

# 관련 문서를 검색하는 노드 만들기
def retrieve(state: AgentState):
    """
    현재 질문을 기반으로 관련 문서를 검색합니다.
    """
    print("----- [RETRIEVER] -----")
    question = state["question"]
    relevant_doc = retriever.invoke(question)
    context = ""
    for doc in relevant_doc:
        context += f"page {doc.metatdat['page']+1}: {doc.page_content}\n"

    # Tool 호출에 대한 응답 메시지(검색 결과) 생성
    last_message = state["messages"][-1]

    if hasattr(last_message, 'tool_calls') and len(last_message.tool_calls) > 0:
        tool_call_id = last_message.tool_calls[0]['id']
        tool_message = ToolMessage(
            content=context,
            name="retriever",
            tool_call_id=tool_call_id
        )
        return {"messages": [tool_message], "context": context}
    else:
        return {"messages": [context], "context": context}

# 검색 결과를 정리하는 노드 만들기
def context_organizer(state: AgentState):
    """
    검색된 결과를 정리합니다.
    """
    print("----- [CONTEXT ORGANIZER] -----")
    context = state["context"]

    context_organizer_prompt = ChatPromptTemplate.from_messages(
        [
            (   "system",
                """당신은 검색증강생성(RAG)을 위한 검색 문서를 정리하는 전문가입니다.
                다음의 검색된 결과 문서를 확인하고, LLM이 해당 문서를 정리된 형태로 참고할 수 있도록
                문서의 불필요한 공백 등을 삭제하거나 정렬을 다시하여 정리된 형태로 반환해주세요.
                내용을 삭제하는 것을 최소로 합니다. 페이지 번호 정보를 절대 삭제하지 마세요."""
            ),
            (
                "user",
                """
                검색 결과: {context}
                """,
            )
        ]
    )

    context_organizer = context_organizer_prompt | llm
    organized_context = context_organizer.invoke({"context": context})

    return{"context": organized_context.content, "messages": [AIMessage (organized_context.content)]}

# 문서와 질문의 관련성을 평가하는 엣지 만들기 (관련성 평가 엣지 구현하기)
from pydantic import BaseModel
from pydantic import Field

class Grade(BaseModel):
    """관련성 확인을 위한 점수 스키마"""

    binary_score: str = Field(description=" 문서가 질문과 관련이 있는지 여부, 'yes' 또는 'no'")

def decide_to_generate(state):
    """
    답변을 생성할지, 아니면 질문을 다시 생성할지 결정합니다.
    """

    print("----- ASSESS GRADED DOCUMENTS -----")
    if state.get("retry_num", 0) >= 3:
        return "generate"

    grader = llm.with_structured_output(Grade)

    grader_prompt = ChatPromptTemplate.from_messages(
        [
            (
                    "system",
                    """
                    당신은 검색된 문서가 사용자 질문과 관련이 있는지 평가하는 평가자입니다.
                    문서가 사용자 질문과 관련된 키워드나 의미를 포함하고 있다면 관련성이 있다고 평가하세요.
                    업격한 테스트일 필요는 없습니다. 목표는 잘못된 검색 결과를 필터링하는 것입니다.
                    문서가 질문과 관련이 있는지를 나타내는 'yes' 또는 'no'의 이진 점수를 제공하세요.
                    """
            ),
            (
                    "user",
                    "검색된 문서: {context} \n\n 사용자 질문: {question} \n\n 관련성 점수:"
            ),
        ]
    )

    chain = grader_prompt | grader

    question = state.get("question", "")
    context = state.get("context", "")

    if not context or not question:
        print("---ERROR: Missing context or question, defaulting to generate---")
        return "generate"

    score = chain.invoke({"question": question, "context": context})
    grade = score.binary_score
    if grade == "no":
        print(
            "---DECISION: RETRIEVED DOCUMENT ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
        )
        return "transform_query"
    else:
        print("---DECISION: GENERATE---")
        return "generate"

# 꼭 이해하고 넘어가기 > LLM의 응답 구조화를 위한 방식 with_structured_output

# 응답을구조화하기 위한 스키마 정의하기
# from pydantic import BaseModel, Field

# class ResponseSchema(BaseModel):
#     """이 클래스는 응답을 구조화하기 위한 예시 스키마입니다."""
#     answer: str = Field(description="사용자 질문에 대한 응답 텍스트")
#     followup_question: str = Field(description="사용자가 이어서 할 수 있는 확장 질문 텍스트")

# with_structured_output을 사용하여 스키마 구조에 맞춰 답변 출력하기

# model_with_structure = model.with_structured_output(ResponseSchema)
# structured_output = model_with_structure.invoke("AI가 글을 쓸 때 사람이 쓴 글과 어떻게 다른가요?")
# structured_output

# 출력 스키마를 도구로 활용하기
# model_with_tools = model.bind_tools(ResponseSchema)
# ai_msg = model_with_tools.invoke("AI가 글을 쓸 때 사람이 쓴 글과 어떻게 다른가요?")
# ai_msg

# 도구의 인자 추출하기
# ai_msg.tool_calls[0]["args"]

# 도구 호출 결과를 파이단틱 객체로 파싱하기
# pydantic_object = ResponseSchema.model_validate(ai_msg.tool_calls[0]["args"])
# pydantic_object

# ---------------------------------------------------

# Query 재작성 노드 만들기
def transform_query(state: AgentState):
    """
    더 나은 질문을 생성하기 위해 쿼리를 변환합니다
    
    Args:
        state (dict): 현재 그래프 상태

    Returns:
        state (dict): 재구성된 질문으로 question 키를 업데이트
    """

    print("----- [TRANSFORM QUERY] -----")
    question = state["question"]

    system = """
    당신은 질문을 다시 작성하는 전문가입니다. 입력된 질문을 벡터 저장소 검색에 최적화된 더 나은 버전으로 변환하세요.
    입력을 살펴보고 질문의 핵심적인 의미와 의도를 파악하여 개선된 질문을 만들어주세요."""
    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "user",
                "다음은 초기 질문입니다: \n\n (question) \n 한국어로 개선된 질문을 작성해주세요."
            ),
        ]
    )

    question_rewriter = re_write_prompt | llm

    better_question = question_rewriter.invoke({"question": question})
    return {
        "question": better_question.content,
        "messages": [better_question],
        "retry_nums": state["retry_num"] + 1 if state.get("retry_num") else 1
    }

# 검색된 문서를 기반으로 답변을 생성하는 노드 만들기
def generate(state: AgentState):
    """
    검색된 문서와 질문을 기반으로 답변을 생성합니다.
    """
    print("----- [GENERATE] -----")
    question = state["question"]
    context = state["context"]

    retry_num = state.get("retry_num", 0)

    if retry_num >= 3:
        rag_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """당신은 검색된 문서를 통해 해결할 수 있는 질문을 추출하는 어시스턴트입니다.
                    사용자가 해결하고자 한 질문이 있었으나 검색 컨텍스트가 충분하지 않은 상황이므로,
                    주어진 검색 결과 내에서 답변할 수 있는 질문을 새롭게 작성해 나열하세요.
                    사용자에게 질문에 대한 답변을 하지 못함에 양해를 구하고, 다른 질문의 기회와
                    선택지를 제공하는 친절한 가이드를 하세요.
                    """,
                ),
                (
                    "user",
                    "질문: {question} \n\n검색 결과: {context} \n\n답변:",
                ),
            ]
        )
    else:
        rag_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """당신은 질문-답변 업무를 수행하는 어시스턴트입니다. 검색된 컨텍스트를 사용하여 질문에 답변하세요.
                    답변을 모르는 경우, 모른다고 말하세요.
                    답변은 간결하게 작성하고, 반드시 답변의 출처(페이지 번호)를 함께 명시해주세요.
                    
                    """,
                ),
                (
                    "user",
                    "질문: {question} \n\n검색 결과: {context} \n\n답변:",
                ),
            ]
        )

    rag_chain = rag_prompt | llm
    response = rag_chain.invoke({"question": question, "context": context})
    return {"question": question, "answer": response.content, "messages": [response]}

# 답변의 환각 여부르 평가하는 라우팅 함수 만들기
class GradeHallucinations(BaseModel):
    """생성된 답변의 환각 여부를 판단하기 위한 점수 스키마"""

    binary_score: str = Field(
        description = "답변이 사실에 근거하는지 여부, 'yes' 또는 'no'"
    )

def check_hallucinations(state):
    """
    생성된 답변이 문서에 근거하고 질문에 답하는지 판단합니다.
    """

    print("----- CHECK HALLUCINATIONS -----")
    question = state["question"]
    context = state["context"]
    answer = state["answer"]

    structured_llm = llm.with_structured_output(GradeHallucinations)

    system = """당신은 LLM이 생성한 답변이 검색된 사실들에 근거하고 있는지 평가하는 평가자입니다.
    'yes' 또는 'no'의 이진 점수를 제공하세요. 'yes'는 답변이 사실들에 근거하고 있음을 의미합니다."""
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("user", "질문: {question} \n\n 사실 집합: \n\n {context} \n\n LLM 생성 답변: {generation}")
        ]
    )

    hallucination_grader = hallucination_prompt | structured_llm

    score = hallucination_grader.invoke(
        {"question": question, "context": context, "generation": answer}
    )
    grade = score.binary_score
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        return "support"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"

# RAG 에이전트를 위한 그래프 만들기
from langgraph.prebuilt import tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END

from state import AgentState
from nodes import chatbot, 