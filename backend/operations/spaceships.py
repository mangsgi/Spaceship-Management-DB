from sqlalchemy.orm import Session
from models import Spaceships, SpaceshipCreate, SpaceshipResponse, Flights
from fastapi import HTTPException
from datetime import datetime, time
from typing import Optional, List

# Fin Administrator - 우주선 생성
def create_spaceship(db: Session, spaceship_data: SpaceshipCreate) -> SpaceshipResponse:
    try:
        db_spaceship = Spaceships()
        db_spaceship.manufacture_date = datetime.strptime(spaceship_data.manufacture_date, "%Y-%m-%d").date()
        db_spaceship.model = spaceship_data.model
        db_spaceship.status = spaceship_data.status
        
        db.add(db_spaceship)
        db.commit()
        db.refresh(db_spaceship)
        return SpaceshipResponse.model_validate(db_spaceship)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"우주선 생성 중 오류 발생: {str(e)}")
    
# Administrator - 우주선 상태 업데이트
def update_spaceship_status(db: Session, spaceship_id: int, new_status: str) -> SpaceshipResponse:
    spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
    if not spaceship:
        raise HTTPException(status_code=404, detail="우주선을 찾을 수 없습니다.")
    
    spaceship.status = new_status
    db.commit()
    db.refresh(spaceship)
    return SpaceshipResponse.model_validate(spaceship)


def get_available_spaceships(
    db: Session, 
    departure_time: Optional[datetime] = None,
    arrival_time: Optional[datetime] = None,
) -> List[Spaceships]:
    # 기존 비행 일정의 시간 안에 겹치지 않는 우주선만 필터링 
    if departure_time and arrival_time:
        query = db.query(Spaceships).filter(
            ~db.query(Flights)
            .filter(
                Flights.spaceship_id == Spaceships.spaceship_id,
                Flights.departure_time < arrival_time,
                Flights.arrival_time > departure_time,
            )
            .exists()
        ).all()
    else:
        query = db.query(Spaceships).all()
    if not query:
        return []
    return query