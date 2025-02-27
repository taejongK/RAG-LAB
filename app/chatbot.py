from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from operator import itemgetter

import os
from dotenv import load_dotenv
import pickle

load_dotenv()

# 1. 저장된 임베딩 모델 불러오기
embedding_model_path = "/home/taejong_kim/workspace/rag-lab/database/embedding_model/hf_embedding_model01.pkl"
vectorstore_path = "/home/taejong_kim/workspace/rag-lab/database/vector_store"

with open(embedding_model_path, "rb") as f:
    embedding_model = pickle.load(f)

# 2. 저장된 벡터스토어 불러오기
vectorstore = FAISS.load_local(
    vectorstore_path, embedding_model, allow_dangerous_deserialization=True)

# 3. retriever 생성
retrieval = vectorstore.as_retriever()

prompt = PromptTemplate.from_template(
    """"You are a support agent. 
Please respond in the same language as the user's input. Detect the language they are using and reply naturally in that language while maintaining clarity and accuracy.

If you don't know the answer, just say that you don't know. 

Use the following pieces of retrieved context to answer the question. 

#Previous Chat History:
{chat_history}

#Question: 
{question} 

#Context: 
{context} 

#Answer:"""
)

# 언어 모델
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

chain = (
    {
        "context": itemgetter("question") | retrieval,
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
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
