from sqlalchemy.orm import Session
from models import Spaceships, SpaceshipCreate, SpaceshipResponse
from fastapi import HTTPException

# Administrator - 우주선 상태 업데이트
def update_spaceship_status(db: Session, spaceship_id: int, new_status: str) -> SpaceshipResponse:
    spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
    if not spaceship:
        raise HTTPException(status_code=404, detail="우주선을 찾을 수 없습니다.")
    
    spaceship.status = new_status
    db.commit()
    db.refresh(spaceship)
    return SpaceshipResponse.model_validate(spaceship)
