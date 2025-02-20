from typing import Dict
from repository import ChatbotRepository
from datetime import datetime
from chatbot import *

uuid2room: Dict[str, str] = {}


def create_chatbot(uuid: str):
    '''
    챗봇 인스턴스를 생성
    '''
    uuid2room[uuid] = SampleCreateResponseService()
    return uuid2room[uuid]


class SampleCreateResponseService:
    '''
    나중에 LLM model로 변경 예정
    '''

    def __init__(self):
        self.repo = ChatbotRepository()  # 대화 내용 저장소 인스턴스 생성

    def create_response(self, request: dict) -> dict:
        uuid = request.uuid
        question = request.query
        # 질문 시간, 정확히는 질문이 넘어온 시간
        question_timestamp = int(datetime.now().timestamp())

        # if question == "안녕":
        #     answer = "안녕하세요"
        #     response_timestamp = int(datetime.now().timestamp()) # 응답 시간
        # else:
        #     answer = "죄송합니다. 이해할 수 없습니다."
        #     response_timestamp = int(datetime.now().timestamp()) # 응답 시간
        answer = chain_with_history.invoke({"question": question},
                                           config={"session_id": uuid})
        # answer = self.chatbot.get_response(question, uuid)
        response_timestamp = int(datetime.now().timestamp())

        # 저장 코드
        self.repo.save_conversation({
            "uuid": uuid,
            "question": question,
            "response": answer,
            "question_timestamp": question_timestamp,
            "response_timestamp": response_timestamp
        })

        return {
            "uuid": uuid,
            "response": answer,
            "response_timestamp": response_timestamp
        }
