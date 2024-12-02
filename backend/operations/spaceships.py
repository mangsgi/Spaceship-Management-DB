from sqlalchemy.orm import Session
from models import Spaceships, SpaceshipCreate, SpaceshipResponse, Flights
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List

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