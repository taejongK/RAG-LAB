from pydantic import BaseModel
from datetime import datetime

'''
데이터 모델 정의
pydantic을 사용해 API 요청 및 응답 데이터를 검증
'''

class ChatHistoryCreate(BaseModel):
    user_id: str
    message: str
    response: str

class ChatHistoryResponse(ChatHistoryCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True  # ORM 객체를 JSON 응답으로 변환
