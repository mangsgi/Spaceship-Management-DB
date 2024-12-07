from sqlalchemy.orm import Session
from models import Spaceships, SpaceshipCreate, SpaceshipResponse, Flights, SpaceshipUpdateRequest
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List

# Fin Administrator - 우주선 생성
def create_spaceship(db: Session, spaceship_data: SpaceshipCreate) -> SpaceshipResponse:
    try:
        db_spaceship = Spaceships(**spaceship_data.model_dump())
        
        db.add(db_spaceship)
        db.commit()
        db.refresh(db_spaceship)
        return SpaceshipResponse.model_validate(db_spaceship)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"우주선 생성 중 오류 발생: {str(e)}")
    
# Administrator - 우주선 상태 업데이트
def update_spaceship_status(db: Session, spaceship_id: int, spaceship_update_data: SpaceshipUpdateRequest) -> SpaceshipResponse:
    spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
    if not spaceship:
        raise HTTPException(status_code=400, detail="우주선을 찾을 수 없습니다.")
    
    if spaceship_update_data.status not in ['운영 중', '점검 중']:
        raise HTTPException(status_code=401, detail=f"Invalid status: {spaceship_update_data.status}. Must be one of {['운영 중', '점검 중']}")
    
    if spaceship_update_data.status is not None:
        spaceship.status = spaceship_update_data.status
    if spaceship_update_data.last_maintenance_date is not None:
        spaceship.last_maintenance_date = spaceship_update_data.last_maintenance_date
    
    db.commit()
    db.refresh(spaceship)
    return SpaceshipResponse.model_validate(spaceship)

# Fin Administrator - 우주선 조회 for 비행 일정 생성과 수정 및 우주선 할당
def get_available_spaceships(
    db: Session, 
    departure_time: Optional[datetime] = None,
    arrival_time: Optional[datetime] = None,
) -> List[Spaceships]:
    # 운영 중인 우주선만 포함
    query = db.query(Spaceships).filter(Spaceships.status == "운영 중")

    # 기존 비행 일정의 시간 안에 겹치지 않는 우주선만 필터링 
    if departure_time and arrival_time:
        query = query.filter(
            ~db.query(Flights)
            .filter(
                Flights.spaceship_id == Spaceships.spaceship_id,
                Flights.departure_time < arrival_time,
                Flights.arrival_time > departure_time,
            )
            .exists()
        )
        
    spaceships = query.all()
    if not spaceships:
        return []
    return [SpaceshipResponse.model_validate(spaceship) for spaceship in spaceships]

def get_spaceships(db: Session, spaceship_id: Optional[int] = None):
    if spaceship_id is not None:
        spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
        if not spaceship:
            raise HTTPException(status_code=404, detail="해당 우주선을 찾을 수 없습니다.")
        return [SpaceshipResponse.model_validate(spaceship)]  # 단일 우주선을 리스트로 반환
    else:
        spaceships = db.query(Spaceships).all()
        return [SpaceshipResponse.model_validate(spaceship) for spaceship in spaceships]