from sqlalchemy.orm import Session
from models import Pilots, PilotCreate, PilotResponse, PilotUpdateRequest
from fastapi import HTTPException

# Pilot - 본인의 개인정보 수정
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
