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

# UPDATE
def update_spaceship(db: Session, spaceship_id: int, spaceship: SpaceshipCreate) -> SpaceshipResponse:
    db_spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
    if not db_spaceship:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    for key, value in spaceship.model_dump().items():
        setattr(db_spaceship, key, value)
    db.commit()
    db.refresh(db_spaceship)
    return db_spaceship

# DELETE
def delete_spaceship(db: Session, spaceship_id: int):
    db_spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == spaceship_id).first()
    if not db_spaceship:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    db.delete(db_spaceship)
    db.commit()
    return {"message": f"Spaceship {spaceship_id} deleted successfully"}
