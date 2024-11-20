# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from database import SessionLocal, engine, Base
from pydantic import BaseModel

app = FastAPI()

origins = [
    # "http://localhost:5000",  # Svelte 기본 포트
    # "http://localhost:3000",  # Svelte 다른 포트 사용 시
    "http://localhost:8080",  # Svelte 다른 포트 사용 시
    # 필요에 따라 다른 도메인 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 또는 ["*"]으로 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 모델 정의
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

# Pydantic 스키마
class ItemCreate(BaseModel):
    title: str
    description: str

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 의존성: 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 엔드포인트
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
