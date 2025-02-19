from sqlalchemy.orm import Session
from models import ChatHistory
from schemas import ChatHistoryCreate

'''
데이터베이스 조작 함수
대화 기록을 저장하고 불러오는 함수
'''

# 새로운 대화 저장
def create_chat_history(db: Session, chat_data: ChatHistoryCreate):
    chat_record = ChatHistory(**chat_data.dict())
    db.add(chat_record)
    db.commit()
    db.refresh(chat_record)
    return chat_record

# 사용자별 대화 기록 조회
def get_chat_history(db: Session, user_id: str, limit: int = 10):
    return db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
