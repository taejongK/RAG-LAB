from typing import Dict
from repository import ChatbotRepository
from datetime import datetime
from chatbot import *


uuid2room: Dict[str, str] = {}


def create_chatbot(uuid: str):
    '''
    챗봇 인스턴스를 생성
    '''
    uuid2room[uuid] = ChatbotService()
    return uuid2room[uuid]


class ChatbotService:
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

        response = chain_with_history.invoke({"question": question},
                                           config={"session_id": uuid})
        answer = response['answer']
        is_context_relevant = response['is_context_relevant'] # 이미지가 필요한가 아닌가?
        
        response_timestamp = int(datetime.now().timestamp())
 
        img_list = self.get_image_path_list(retrieval, question)

        # 저장 코드
        self.repo.save_conversation({
            "uuid": uuid,
            "question": question,
            "response": answer,
            "question_timestamp": question_timestamp,
            "response_timestamp": response_timestamp,
            'response_image_list': img_list
        })

        return {
            "uuid": uuid,
            "response": answer,
            "response_timestamp": response_timestamp,
            "images": img_list,
            "is_context_relevant": is_context_relevant
        }

    def get_image_path_list(self, retrieval, question):
        """
        retrieval에서 검색과 관련된 리스트 경로 반환환
        """
        img_list = []  # 출력해야할 이미지 리스트트

        for doc in retrieval.invoke(question):
            img_path = doc.metadata["images"]
            if len(img_path) > 0:
                for img in img_path:
                    img_list.append(img)
        return img_list