from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from database import SessionLocal, engine, Base
from pydantic import BaseModel

app = FastAPI() # API 엔드포인트와 설정이 이 객체에 연결

origins = [ # CORS를 설정하여, 다른 도메인에서의 API 요청을 허용
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

# 데이터베이스 모델 정의
class Item(Base):
    __tablename__ = "items" # Item 클래스를 items table에 매핑
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

# Pydantic 모델 정의, API 요청 시 데이터를 검증하고 구조화
class ItemCreate(BaseModel): # 새 아이템을 생성할 때 사용하는 Request 모델
    title: str
    description: str

class ItemResponse(BaseModel): # 데이터베이스 ORM 객체를 반환할 때 사용하는 Response 모델
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True # orm_mode replaces from_attributes in pydantic 2.0.0 over version 

# 데이터베이스 테이블 생성 및 초기화
Base.metadata.create_all(bind=engine)

# 의존성: 데이터베이스 세션 생성
def get_db(): # API 엔드포인트에서 데이터베이스 세션을 가져옴
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 엔드포인트
@app.post("/items/", response_model=ItemResponse) # 새 아이템 생성
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    ''' 
    ItemCreate로 요청 데이터를 받고, db 세션을 사용하여 데이터베이스에 저장
    새로 추가된 항목을 반환
    '''
    db_item = Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)): # 아이템 조회
    ''' 
    item_id를 사용하여 특정 아이템을 조회
    해당 항목이 없으면 404 오류를 반환
    '''
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
