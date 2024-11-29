from sqlalchemy.orm import Session
from models import Flights, FlightCreate, FlightResponse, FlightUpdateRequest
from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy import Date

# Administrator - 비행 일정 생성
def create_flight(db: Session, flight: FlightCreate) -> FlightResponse:
    try:
        db_flight = Flights(**flight.model_dump())
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return db_flight
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"비행 일정 생성 중 오류 발생: {str(e)}")

# READ ALL
def get_all_flights(db: Session) -> list[FlightResponse]:
    return db.query(Flights).all()

# Administrator - 비행 일정 수정 
def update_flight_information(
    db: Session, flight_id: int, flight_data: FlightUpdateRequest
) -> FlightResponse:
    
    flight = db.query(Flights).filter(Flights.flight_id == flight_id).first()
    
    if not flight:
        raise HTTPException(status_code=404, detail="비행 일정을 찾을 수 없습니다.")
    try:
        # Update only the fields provided in the request
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

# Customer - 비행 일정 조회
def search_flights(
    db: Session,
    departure_location: Optional[str] = None,
    arrival_location: Optional[str] = None,
    departure_date: Optional[str] = None,
    sort_by: Optional[str] = "departure_time"
) -> List[FlightResponse]:
    
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