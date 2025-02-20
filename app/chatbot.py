from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

import os
from dotenv import load_dotenv

load_dotenv()


# 대화 내용 기억하기
system_prompt = """
"You are a support agent. 
Please respond in the same language as the user's input. Detect the language they are using and reply naturally in that language while maintaining clarity and accuracy."
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{question}"),  # 사용자 입력을 변수로 사용
    ]
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

# langchain
chain = (
    prompt
    | llm
    | StrOutputParser()
)


# 세션 기록을 저장할 딕셔너리
store = {}


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_id):
    print(f"Session ID: {session_id}")
    if session_id not in store:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[session_id] = ChatMessageHistory()
    return store[session_id]  # 해당 세션 ID에 대한 세션 기록 반환


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,  # 세션 기록을 가져오는 함수
    input_messages_key="question",  # 사용자의 질문이 템플릿 변수에 들어갈 key
    history_messages_key="chat_history",  # 기록 메시지의 키
)
