from sqlalchemy.orm import Session
from models import Pilots, PilotCreate, PilotResponse, PilotUpdateRequest
from fastapi import HTTPException

# CREATE
def create_pilot(db: Session, pilot: PilotCreate) -> PilotResponse:
    db_pilot = Pilots(**pilot.model_dump())
    db.add(db_pilot)
    db.commit()
    db.refresh(db_pilot)
    return db_pilot

# READ ALL
def get_all_pilots(db: Session) -> list[PilotResponse]:
    return db.query(Pilots).all()

# UPDATE
def update_pilot(db: Session, pilot_id: int, pilot: PilotCreate) -> PilotResponse:
    db_pilot = db.query(Pilots).filter(Pilots.pilot_id == pilot_id).first()
    if not db_pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    for key, value in pilot.model_dump().items():
        setattr(db_pilot, key, value)
    db.commit()
    db.refresh(db_pilot)
    return db_pilot

# DELETE
def delete_pilot(db: Session, pilot_id: int):
    db_pilot = db.query(Pilots).filter(Pilots.pilot_id == pilot_id).first()
    if not db_pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    db.delete(db_pilot)
    db.commit()
    return {"message": f"Pilot {pilot_id} deleted successfully"}

# UPDATE Pilot Information
def update_pilot_information(db: Session, pilot_id: int, pilot_data: PilotUpdateRequest):
    pilot = db.query(Pilots).filter(Pilots.pilot_id == pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=404, detail="파일럿을 찾을 수 없습니다.")
    
    if pilot_data.name is not None:
        pilot.name = pilot_data.name
    if pilot_data.contact_info is not None:
        pilot.contact_info = pilot_data.contact_info
    if pilot_data.emergency_contact is not None:
        pilot.emergency_contact = pilot_data.emergency_contact

    db.commit()
    db.refresh(pilot)
    return pilot
