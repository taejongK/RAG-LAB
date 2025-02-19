from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from service import *

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


class CreateChatBot(BaseModel):
    uuid: str # 생성하고자 하는 ID


class RequestResponse(BaseModel):
    uuid: str # 존재하는 ID
    query: str # 질문
    
class DeleteChatBot(BaseModel):
    uuid: str # 삭제하고자 하는 ID

# 챗봇 생성 요청
@router.post("/chatbot/create/{uuid}")
async def request_create_chatbot(request: CreateChatBot):
    '''
    uuid: str 를 보내면 해당 uuid 를 가진 방을 생성합니다.
    '''
    if request.uuid in uuid2room:
        raise HTTPException(status_code=400, detail=f"{request.uuid} already exists")
    
    chatbot = create_chatbot(request.uuid) # 챗봇 인스턴스 생성
    return {"uuid": request.uuid, "room": chatbot}

# 챗봇 응답 요청
@router.post("/chatbot/response/{uuid}")
async def request_chatbot_response(request: RequestResponse):
    '''
    uuid: str 를 보내면 해당 uuid 를 가진 방에 챗봇이 응답합니다.
    response:
        uuid: uuid
        response: 응답
        response_timestamp: 응답 시간
    '''
    if request.uuid not in uuid2room:
        raise HTTPException(status_code=400, detail="uuid does not exist")

    chatbot = uuid2room[request.uuid]
    
    response = chatbot.create_response(request)

    return response

# 챗봇 삭제 요청
@router.post("/chatbot/delete/{uuid}")
async def request_delete_chatbot(request: DeleteChatBot):
    '''
    uuid: str 를 보내면 해당 uuid 를 가진 방을 삭제합니다.
    '''
    if request.uuid not in uuid2room:
        raise HTTPException(status_code=400, detail="uuid does not exist")
    
    del uuid2room[request.uuid]
    return {"uuid": request.uuid, "status": "deleted"}