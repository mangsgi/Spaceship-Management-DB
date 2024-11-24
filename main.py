from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Date, Enum, Float, DateTime
from database import SessionLocal, engine, Base
import models

app = FastAPI() # API 엔드포인트와 설정이 이 객체에 연결

origins = [ # CORS를 설정하여, 다른 도메인에서의 API 요청을 허용
    # "http://localhost:5000",  # Svelte 기본 포트
    # "http://localhost:3000",  # Svelte 다른 포트 사용 시
    "http://localhost:8080",  # Svelte 다른 포트 사용 시
    # "http://localhost:8000",  # uvicorn 기본 포트
    # 필요에 따라 다른 도메인 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 또는 ["*"]으로 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.get("/")
def read_root():
    return {"message": "Database initialized with tables!"}

# CREATE: 조종사 생성
@app.post("/pilots/", response_model=models.PilotResponse)
def create_pilot(pilot: models.PilotCreate, db: Session = Depends(get_db)):
    db_pilot = models.Pilots(**pilot.model_dump())  # Pydantic 데이터를 SQLAlchemy 모델로 변환
    db.add(db_pilot)
    db.commit()
    db.refresh(db_pilot)
    return db_pilot

# READ: 조종사 조회
@app.get("/pilots/{pilot_id}", response_model=models.PilotResponse)
def read_pilot(pilot_id: int, db: Session = Depends(get_db)):
    db_pilot = db.query(models.Pilots).filter(models.Pilots.pilot_id == pilot_id).first()
    if not db_pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return db_pilot

# UPDATE: 조종사 정보 수정
@app.put("/pilots/{pilot_id}", response_model=models.PilotResponse)
def update_pilot(pilot_id: int, pilot: models.PilotCreate, db: Session = Depends(get_db)):
    db_pilot = db.query(models.Pilots).filter(models.Pilots.pilot_id == pilot_id).first()
    if not db_pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    
    for key, value in pilot.model_dump().items():
        setattr(db_pilot, key, value)
    
    db.commit()
    db.refresh(db_pilot)
    return db_pilot

# DELETE: 조종사 삭제
@app.delete("/pilots/{pilot_id}")
def delete_pilot(pilot_id: int, db: Session = Depends(get_db)):
    db_pilot = db.query(models.Pilots).filter(models.Pilots.pilot_id == pilot_id).first()
    if not db_pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    
    db.delete(db_pilot)
    db.commit()
    return {"message": f"Pilot {pilot_id} deleted successfully"}