## Release Notes

### v0.1.0
2025.02.26 
- ChatBot 기능 구현
- 이미지 출력 기능 구현
- 대화 내용 저장 기능 구현
- ChatBot 삭제 router 구현 -> 실제 기능 미구현 v0.2.0 예정

### ver0.2.0
2025.02.27
- README chatbot 부분 수정
- pdf2markdown 모듈 구현
- 이미지 출력 기능 수정
  - 사용자의 질문이 retriever로 검색된 내용과 관련이 없으면 이미지 출력하지 않음
  - json parser를 사용해서 답변에서 이미지 출력이 필요한지 True/False로 반환하도록 수정