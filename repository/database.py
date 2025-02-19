from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

'''
데이터베이스 설정
SQLite 데이터베이스 연결을 설정합니다.
'''

DATABASE_URL = "sqlite:///./chatbot.db"

# SQLite 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델 베이스 클래스
Base = declarative_base()
