import streamlit as st
import requests
import uuid

from main import *

############################# 챗봇 생성 #############################
if "uuid" not in st.session_state:
    # uuid 생성
    uuid = str(uuid.uuid4())  # 임시생성 uuid
    st.session_state.uuid = uuid

    # 새션 만들기
    session_url = f"http://127.0.0.1:8000/chatbot/create/{uuid}"
    params = {"uuid": uuid}
    session = requests.post(session_url, json=params)
    print("session result: ", session.json()['uuid'])
    
uuid = st.session_state.uuid
############################# 챗팅 페이지 #############################
# 페이지 제목
st.title("RAG ChatBot")

# 세션 상태에 채팅 기록 저장 (앱이 새로고침되면 유지)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    # 사용자 메시지를 상태에 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 화면에 표시
    with st.chat_message("user"):
        st.markdown(user_input)

    ##### 간단한 응답 예제 (실제 AI 모델과 연동 가능) #####
    answer_url = f"http://127.0.0.1:8000/chatbot/{uuid}"
    params = {"uuid": uuid, "query": user_input}

    answer = requests.post(answer_url, json=params)
    bot_response = answer.json()['response']
    # print('bot_response: ',bot_response)

    ########################################################

    # 챗봇 응답을 상태에 추가
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response})
    # print(st.session_state.messages)

    # 챗봇 응답 표시
    with st.chat_message("assistant"):
        st.markdown(bot_response)
