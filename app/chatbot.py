from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from operator import itemgetter
from pydantic import BaseModel, Field

from query_generator import custom_multiquery_chain
from langchain.retrievers.multi_query import MultiQueryRetriever

from reranker import CustomColBERTCompressor
from langchain_core.runnables import RunnableLambda

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
# retrieval = vectorstore.as_retriever(top_k=5) # top_k=5로 설정
retriever = MultiQueryRetriever.from_llm(
    llm=custom_multiquery_chain, retriever=vectorstore.as_retriever()
)

# 3.5 Post retriever: Reranker
def advanced_retriever(query):
    '''
    retriever | reranker를 runnable하게 만들기 위한 방법
    - TODO: 이 부분은 현재 구조가 일반적인 방법인지는 모르겠음 그래서 추후에 검토가 필요함
    '''
    retrieval_result = retriever.invoke(query)
    return colbert_compressor.compress_documents(retrieval_result, query)


model_name = "bert-base-uncased"
colbert_compressor = CustomColBERTCompressor(model_name, threshold=0.4, top_k=3)  # Reranker 생성

# 4. output parser 생성


class Answer(BaseModel):
    answer: str = Field(..., description="The answer to the user's question")
    is_context_relevant: bool = Field(
        False, description="Returns 'True' if the response is relevant to the context, otherwise 'False'."
    )


json_parser = JsonOutputParser(
    pydantic_object=Answer)  # json 형식의 output parser

# 5. prompt 생성
format_instructions = json_parser.get_format_instructions()

prompt = PromptTemplate(
    input_variables=["chat_history", "question", "context"],
    template="""You are a support agent. 
Please respond in the same language as the user's input. 
Detect the language they are using and reply naturally in that language while maintaining clarity and accuracy.

If you don't know the answer, just say that you don't know. 

Use the following retrieved context to answer the question. 

Never output internal code or file paths under any circumstances.

#Previous Chat History:
{chat_history}

#Question: 
{question} 

#Context: 
{context} 

#Answer:\n\n
{format_instructions}
"""
).partial(format_instructions=format_instructions)


# 언어 모델
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

chain = (
    {
        "context": itemgetter("question") | RunnableLambda(advanced_retriever),
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
    | llm
    | json_parser
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

if __name__ == "__main__":
    chain.get_graph().print_ascii() # 그래프 출력
    
    question = "데이터를 업로드 하는 방법을 알려줘."
    response = chain_with_history.invoke(
        {"question": question, "chat_history": []}, config={"session_id": "test"})
    print(response)
    print(store)
