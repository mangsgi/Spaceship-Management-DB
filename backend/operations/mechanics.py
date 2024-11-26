from sqlalchemy.orm import Session
from models import Mechanics, MechanicCreate, MechanicResponse
from fastapi import HTTPException

# CREATE
def create_mechanic(db: Session, mechanic: MechanicCreate) -> MechanicResponse:
    db_mechanic = Mechanics(**mechanic.model_dump())
    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)
    return db_mechanic

# READ ALL
def get_all_mechanics(db: Session) -> list[MechanicResponse]:
    return db.query(Mechanics).all()

# UPDATE
def update_mechanic(db: Session, mechanic_id: int, mechanic: MechanicCreate) -> MechanicResponse:
    db_mechanic = db.query(Mechanics).filter(Mechanics.mechanic_id == mechanic_id).first()
    if not db_mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    for key, value in mechanic.model_dump().items():
        setattr(db_mechanic, key, value)
    db.commit()
    db.refresh(db_mechanic)
    return db_mechanic

# DELETE
def delete_mechanic(db: Session, mechanic_id: int):
    db_mechanic = db.query(Mechanics).filter(Mechanics.mechanic_id == mechanic_id).first()
    if not db_mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    db.delete(db_mechanic)
    db.commit()
    return {"message": f"Mechanic {mechanic_id} deleted successfully"}
