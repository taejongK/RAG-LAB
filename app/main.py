from fastapi import FastAPI
from router import router
from repository import *

app = FastAPI()

app.include_router(router)

# 테이블 생성
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    