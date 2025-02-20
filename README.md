# RAG-ChatBot
## 0. 실행 방법
```
cd app
python main.py
```

다른 터미널 창에서 아래 명령어를 실행합니다.

```
cd app
streamlit run client.py
```

## 1. 프로젝트 소개
- RAG(Reformulated Attention Generator) 모델을 활용한 ChatBot입니다.
- fast-api로 언어 모델 api 개발
- streamlit으로 웹 페이지 개발

## 2. 프로젝트 구조

### 2.1. Router(Endpoint)
- `GET /`: 웹 페이지
- `/chatbot/create/{uuid}`: 챗봇 생성
- `/chatbot/response/{uuid}`: 챗봇 대화
- `/chatbot/delete/{uuid}`: 챗봇 삭제

### 2.2. Service
- create_chatbot: 챗봇 생성
- response_chatbot: 질문을 받으면 답을 주는 챗봇
- delete_chatbot: 챗봇 삭제(미구현)

### 2.3. Repository
- ChatHistory
    - id: Primary Key
    - uuid: ChatBot 인스턴스 별로 부여
    - question: 사용자의 질문
    - answer: LLM의 답변
    - question_time: 질문 시간
    - answer_time: 답변 시간



## 3. Model
### 3.1 Enbedding
- hugging face -> "jhgan/ko-sroberta-multitask"

### 3.2 LLM
- google gemini 1.5 pro 

### 3.3 Retriever
- 미구현현