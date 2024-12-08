import toml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

secrets = toml.load("../secrets.toml")

engine = create_engine(secrets['DATABASE_URL']) # 데이터베이스와 연결 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 데이터베이스와의 세션 생성

Base = declarative_base() # ORM을 위한 베이스 클래스, 테이블 모델 정의 시 이 클래스 상속