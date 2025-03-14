from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_ollama import ChatOllama

# 프롬프트 템플릿을 정의합니다.(5개의 질문을 생성하도록 프롬프트를 작성하였습니다)
gen_query_prompt = PromptTemplate.from_template(
    """You are an AI language model assistant. 
Your task is to generate five different versions of the given user question to retrieve relevant documents from a vector database. 
By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. 
Your response should be a list of values separated by new lines, eg: `foo\nbar\nbaz\n`

#ORIGINAL QUESTION: 
{question}

#Answer in Korean:
"""
)

llm4query = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b")
# llm4query = ChatOllama(model='exaone3.5:2.4b')

custom_multiquery_chain = (
    {"question": RunnablePassthrough()} 
    | gen_query_prompt 
    | llm4query 
    | StrOutputParser()
)

if __name__ == "__main__":
    # 질문을 정의합니다
    question = "OpenAI Assistant API의 Functions 사용법에 대해 알려주세요."

    # 체인을 실행하여 생성된 다중 쿼리를 확인합니다.
    multi_queries = custom_multiquery_chain.invoke({"question": question})
    print(multi_queries)