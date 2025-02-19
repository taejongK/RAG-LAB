from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

'''
chat_history 테이블 모델 정의
SQLAlchemy를 사용해 caht_history 테이블을 생성성
'''

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    message = Column(Text, nullable=False)  # 사용자 입력
    response = Column(Text, nullable=False)  # 챗봇 응답
    timestamp = Column(DateTime, default=func.now())  # 메시지 시간 자동 추가
