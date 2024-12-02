from sqlalchemy.orm import Session
from models import Flights, FlightCreate, FlightResponse, FlightUpdateRequest, Pilots, PilotFlights
from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy import Date, not_
from datetime import datetime

# Administrator - 비행 일정 생성
def create_flight(db: Session, flight: FlightCreate) -> FlightResponse:
    try:
        db_flight = Flights(**flight.model_dump())
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return FlightResponse.model_validate(db_flight)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"비행 일정 생성 중 오류 발생: {str(e)}")

# Administrator - 비행 일정 수정 
def update_flight_information(db: Session, flight_id: int, flight_data: FlightUpdateRequest) -> FlightResponse:
    flight = db.query(Flights).filter(Flights.flight_id == flight_id).first()
    
    if not flight:
        raise HTTPException(status_code=404, detail="비행 일정을 찾을 수 없습니다.")
    try:
        if flight_data.departure_location is not None:
            flight.departure_location = flight_data.departure_location
        if flight_data.arrival_location is not None:
            flight.arrival_location = flight_data.arrival_location
        if flight_data.departure_time is not None:
            flight.departure_time = flight_data.departure_time
        if flight_data.arrival_time is not None:
            flight.arrival_time = flight_data.arrival_time
        if flight_data.status is not None:
            flight.status = flight_data.status

        db.commit()
        db.refresh(flight)
        return FlightResponse.model_validate(flight)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"비행 일정 수정 중 오류 발생: {str(e)}")

# Administrator - 비행 일정 삭제
def delete_flight(db: Session, flight_id: int):
    flight = db.query(Flights).filter(Flights.flight_id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="비행 일정을 찾을 수 없습니다.")
    try:
        db.delete(flight)
        db.commit()
        return {"message": f"비행 일정 ID {flight_id}가 삭제되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"비행 일정 삭제 중 오류 발생: {str(e)}")

# Pilot - 자신에게 할당된 비행 일정 조회
def read_pilot_flights(db: Session, pilot_id: int, is_current: Optional[bool] = False) -> List[FlightResponse]:
    # Pilot 존재 확인
    pilot_exists = db.query(Pilots).filter(Pilots.pilot_id == pilot_id).first()
    if not pilot_exists:
        raise HTTPException(status_code=400, detail="해당 조종사가 존재하지 않습니다.")

    # 비행 일정 불러오기
    query = (
        db.query(Flights)
        .join(PilotFlights, Flights.flight_id == PilotFlights.flight_id)
        .filter(PilotFlights.pilot_id == pilot_id)
    )

    # 현재 이후 일정만 확인
    if is_current:
        current_time = datetime.now()
        query = query.filter(Flights.departure_time <= current_time, Flights.arrival_time >= current_time)

    flights = query.all()

    if not flights:
        return []
    return [FlightResponse.model_validate(flight) for flight in flights]

# Customer - 비행 일정 조회
def search_flights(
    db: Session,
    departure_location: Optional[str] = None,
    arrival_location: Optional[str] = None,
    departure_date: Optional[str] = None,
    sort_by: Optional[str] = "departure_time"
) -> list[FlightResponse]:
    
    query = db.query(Flights)

    # 필터 조건
    if departure_location:
        query = query.filter(Flights.departure_location == departure_location)
    if arrival_location:
        query = query.filter(Flights.arrival_location == arrival_location)
    if departure_date:
        query = query.filter(Flights.departure_time.cast(Date) == departure_date)

    # 정렬 조건
    if sort_by == "departure_time":
        query = query.order_by(Flights.departure_time)
    elif sort_by == "arrival_time":
        query = query.order_by(Flights.arrival_time)

    flights = query.all()
    return [FlightResponse.model_validate(flight) for flight in flights]

# Fin Administrator - 조종사가 할당되지 않은 비행 일정 조회 to 조종사 할당
def get_unassigned_flights(db: Session) -> List[FlightResponse]:
    unassigned_flights = (
        db.query(Flights)
        .filter(
            not_(
                db.query(PilotFlights.flight_id)
                .filter(PilotFlights.flight_id == Flights.flight_id)
                .exists()
            )
        )
        .all()
    )

    if not unassigned_flights:
        return []
    return [FlightResponse.model_validate(flight) for flight in unassigned_flights]