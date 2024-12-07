from sqlalchemy.orm import Session
from models import Pilots, PilotCreate, PilotResponse, PilotUpdateRequest, Flights, PilotFlights, Licenses
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List
from . import user_roles

# * - 조종사 생성
def create_pilot(db: Session, pilot_data: PilotCreate):
    new_pilot = Pilots(**pilot_data.model_dump())
    db.add(new_pilot)
    db.commit()
    db.refresh(new_pilot)

    user_roles.create_user_role(db, role="조종사", user_id=new_pilot.pilot_id, user_type="조종사")
    return new_pilot

# FIN Pilot - 조회 for 접속
def get_pilot(db: Session, pilot_id: int) -> PilotResponse:
    pilot = db.query(Pilots).filter(Pilots.pilot_id == pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=400, detail="Pilot을 찾을 수 없습니다.")
    return PilotResponse.model_validate(pilot)

# Administrator - 라이선스가 있는 모든 조종사 조회 -> 비행 일정 생성 및 조종사 할당
def get_available_pilots(
    db: Session, 
    departure_time: Optional[datetime] = None, 
    departure_location: Optional[str] = None
) -> List[Pilots]:
    # 라이선스가 있는 조종사 조회
    pilots = (
        db.query(Pilots)
        .join(Licenses, Pilots.pilot_id == Licenses.pilot_id)
        .filter(
            Licenses.license_status == "허가",
            Licenses.license_expiry_date >= datetime.now()
        )
        .all()
    )

    available_pilots = []
    for pilot in pilots:
        # 조종사의 마지막 비행 위치와 시간 확인
        last_flight = ( 
            db.query(Flights)
            .join(PilotFlights, Flights.flight_id == PilotFlights.flight_id)
            .filter(PilotFlights.pilot_id == pilot.pilot_id)
            .order_by(Flights.arrival_time.desc())
            .first()
        )

        # 주어진 출발 시간이나 출발 위치가 없거나 조종사의 마지막 비행 내용이 없으면 추가
        if (not departure_time and not departure_location) or not last_flight:
            available_pilots.append(pilot)
            continue

        # 조건에 맞으면 추가
        if last_flight.arrival_time <= departure_time and last_flight.arrival_location == departure_location:
            available_pilots.append(pilot)
            
    if not available_pilots:
        return []
    return [PilotResponse.model_validate(available_pilot) for available_pilot in available_pilots]

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
    return PilotResponse.model_validate(pilot)

# Fin * - 조종사 삭제
def delete_pilot(db: Session, pilot_id: int):
    pilot = db.query(Pilots).filter(Pilots.pilot_id == pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=401, detail="조종사를 찾을 수 없습니다.")
    try:
        db.delete(pilot)
        db.commit()
        return {"message": f"조종사 '{pilot_id}'가 삭제되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"조종사 삭제 중 오류 발생: {str(e)}")