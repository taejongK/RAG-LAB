from pathlib import Path
import pymupdf4llm
import re
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os
from dotenv import load_dotenv
import pickle

load_dotenv()


## PATH ##
ROOT = os.getcwd()
FILE_PATH = "database/BA_사용메뉴얼_분석가.pdf"
IMG_CONTENT_PATH = os.path.join(ROOT, "database/image")

VECTORSTORE_PATH = "database/vector_store"
EMBEDDING_MODEL_PATH = "database/embedding_model" + "/hf_embedding_model01.pkl"


def extract_images_and_create_documents(text):
    """
    Markdown 텍스트에서 ![]() 형식의 이미지를 추출하고, 
    본문과 이미지 리스트를 LangChain Document 객체로 변환
    """
    # 이미지 패턴 탐색 (예: ![alt text](image_url))
    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

    # 이미지 리스트 추출
    images = image_pattern.findall(text)

    # 본문에서 이미지 태그 제거
    cleaned_text = image_pattern.sub('', text).strip()

    # LangChain Document 생성
    return Document(page_content=cleaned_text, metadata={"images": images})


if __name__ == "__main__":
    # pdf2markdown
    md_text = pymupdf4llm.to_markdown(
        FILE_PATH, write_images=True, image_path=IMG_CONTENT_PATH)

    # split markdown
    splited_markdonw = [item for item in re.split(
        r'(?<!##)##(?!##)', md_text) if item != '']

    # markdown to document object
    docs4md = []
    for md in splited_markdonw:
        doc = extract_images_and_create_documents(md)
        docs4md.append(doc)

    print("Complete convert PDF2Markdown")

    hf = HuggingFaceEmbeddings(
        model_name='jhgan/ko-sroberta-multitask')  # embedding model

    vectorstore = FAISS.from_documents(docs4md, embedding=hf)  # vector store
    retriever = vectorstore.as_retriever()

    vectorstore.save_local(VECTORSTORE_PATH)

    # create embedding model path
    if not os.path.exists(os.path.dirname(EMBEDDING_MODEL_PATH)):
        os.makedirs(os.path.dirname(EMBEDDING_MODEL_PATH))

    with open(EMBEDDING_MODEL_PATH, "wb") as f:
        pickle.dump(hf, f)
    print("Complete save data")
