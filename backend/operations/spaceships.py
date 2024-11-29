from sqlalchemy.orm import Session
from models import Spaceships, SpaceshipCreate, SpaceshipResponse
from fastapi import HTTPException

# CREATE
def create_spaceship(db: Session, spaceship: SpaceshipCreate) -> SpaceshipResponse:
    db_spaceship = Spaceships(**spaceship.model_dump())
    db.add(db_spaceship)
    db.commit()
    db.refresh(db_spaceship)
    return db_spaceship

# READ ALL
def get_all_spaceships(db: Session) -> list[SpaceshipResponse]:
    return db.query(Spaceships).all()

# Administrator - 우주선 상태 업데이트
def update_spaceship_status(db: Session, spaceship_id: int, new_status: str) -> SpaceshipResponse:
    spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
    if not spaceship:
        raise HTTPException(status_code=404, detail="우주선을 찾을 수 없습니다.")
    
    spaceship.status = new_status
    db.commit()
    db.refresh(spaceship)
    return SpaceshipResponse.model_validate(spaceship)

# DELETE
def delete_spaceship(db: Session, spaceship_id: int):
    db_spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
    if not db_spaceship:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    db.delete(db_spaceship)
    db.commit()
    return {"message": f"Spaceship {spaceship_id} deleted successfully"}
