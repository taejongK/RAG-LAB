from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from datetime import datetime
import time
import os

current_path = os.getcwd()  # 현재 경로
parent_path = os.path.dirname(current_path)  # 상위 경로 -> project root
database_path = os.path.join(parent_path, 'database')  # db path
conversation_database_path = os.path.join(
    database_path, 'conversation')  # conversation db 저장소

# 데이터베이스 설정
date = datetime.now().strftime("%Y-%m-%d")
conversation_db_name = f"conversation_{date}.db"
conversation_save_path = os.path.join(
    conversation_database_path, conversation_db_name)
DATABASE_URL = f"sqlite:///{conversation_save_path}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 🟢 1️⃣ 채팅 기록 테이블 모델 정의


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 자동 증가 PK
    uuid = Column(String, nullable=False, index=True)  # 챗팅룸 ID
    question = Column(Text, nullable=False)  # 사용자 질문
    response = Column(Text, nullable=False)  # 챗봇 응답
    question_timestamp = Column(
        String, default=lambda: str(time.time()))  # 질문 시간
    response_timestamp = Column(
        String, default=lambda: str(time.time()))  # 응답 시간


class ChatbotRepository:
    def save_conversation(self, data: dict):
        """
        사용자와 봇의 대화 내용을 저장하는 메서드.
        """
        with SessionLocal() as db:  # 필요한 순간에만 세션을 생성(자동 닫힘)
            new_chat = ChatHistory(
                uuid=data["uuid"],
                question=data["question"],
                response=data["response"],
                question_timestamp=data["question_timestamp"],
                response_timestamp=data["response_timestamp"],
            )
            db.add(new_chat)  # db에 추가
            db.commit()  # db 저장

    def get_history(self):
        """
        저장된 채팅 내역을 반환하는 메서드.
        """
        with SessionLocal() as db:  # ✅ 자동 세션 관리
            return db.query(ChatHistory).all()
