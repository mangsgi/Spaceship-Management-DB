from sqlalchemy.orm import Session
from models import PilotFlights, PilotFlightCreate, PilotFlightResponse, Pilots, Flights
from fastapi import HTTPException
from datetime import datetime

# Pilot - 자신에게 할당된 비행 일정 조회
def read_pilot_flights(db: Session, pilot_id: int, is_current: bool) -> list[PilotFlightResponse]:
    pilot_exists = db.query(Pilots).filter(Pilots.pilot_id == pilot_id).first()
    if not pilot_exists:
        raise HTTPException(status_code=400, detail="해당 조종사가 존재하지 않습니다.")
    schedules = (
        db.query(PilotFlights)
        .filter(PilotFlights.pilot_id == pilot_id)
        .all()
    )
    if is_current: # 현재 기준 비행 일정 조회
        schedules = schedules.query() 
    if not schedules:
        return []
    return [PilotFlightResponse.model_validate(schedule) for schedule in schedules]

# Administrator - 조종사 할당
def assign_pilot_to_flight(db: Session, pilot_flight_data: PilotFlightCreate) -> PilotFlightResponse:
    # 해당 비행 일정이 존재하는지 확인
    flight = db.query(Flights).filter(Flights.flight_id == pilot_flight_data.flight_id).first()
    if not flight:
        raise HTTPException(status_code=400, detail="비행 일정을 찾을 수 없습니다.")

    # 해당 파일럿이 존재하는지 확인
    pilot = db.query(Pilots).filter(Pilots.pilot_id == pilot_flight_data.pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=401, detail="조종사를 찾을 수 없습니다.")

    # 스케줄이 겹치는지 확인
    conflicting_schedule = (
        db.query(PilotFlights)
        .join(Flights, PilotFlights.flight_id == Flights.flight_id)
        .filter(
            PilotFlights.pilot_id == pilot_flight_data.pilot_id,
            Flights.departure_time < flight.arrival_time,
            Flights.arrival_time > flight.departure_time,
        )
        .first()
    )
    if conflicting_schedule:
        raise HTTPException(status_code=402, detail="해당 조종사는 이미 다른 비행 일정에 배정되어 있습니다.")

    # 조종사 할당
    try:
        new_pilot_flight = PilotFlights(
            flight_id=pilot_flight_data.flight_id,
            pilot_id=pilot_flight_data.pilot_id,
        )
        db.add(new_pilot_flight)
        db.commit()
        db.refresh(new_pilot_flight)
        return PilotFlightResponse.model_validate(new_pilot_flight)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=403, detail=f"조종사 할당 중 오류가 발생했습니다: {str(e)}")
