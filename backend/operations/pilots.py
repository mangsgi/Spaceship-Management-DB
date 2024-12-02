from sqlalchemy.orm import Session, joinedload
from models import Pilots, PilotCreate, PilotResponse, PilotUpdateRequest, Flights, PilotFlights, Licenses
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List

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

# Administrator - 라이선스가 있는 모든 파일럿 조회 -> 비행 일정 생성 및 파일럿 할당
def get_available_pilots(
    db: Session, 
    departure_time: Optional[datetime] = None, 
    departure_location: Optional[str] = None
) -> List[Pilots]:
    # 라이선스가 있는 파일럿 조회
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
        # 파일럿의 마지막 비행 위치와 시간 확인
        last_flight = ( 
            db.query(Flights)
            .join(PilotFlights, Flights.flight_id == PilotFlights.flight_id)
            .filter(PilotFlights.pilot_id == pilot.pilot_id)
            .order_by(Flights.arrival_time.desc())
            .first()
        )

        # 주어진 출발 시간이나 출발 위치가 없거나 파일럿의 마지막 비행 내용이 없으면 추가
        if (not departure_time and not departure_location) or not last_flight:
            available_pilots.append(pilot)
            continue

        # 조건에 맞으면 추가
        if last_flight.arrival_time <= departure_time and last_flight.arrival_location == departure_location:
            available_pilots.append(pilot)
            
    if not available_pilots:
        return []
    return available_pilots