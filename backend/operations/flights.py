from sqlalchemy.orm import Session
from models import Flights, FlightCreate, FlightResponse
from fastapi import HTTPException

# CREATE
def create_flight(db: Session, flight: FlightCreate) -> FlightResponse:
    db_flight = Flights(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

# READ
def get_all_flights(db: Session) -> list[FlightResponse]:
    return db.query(Flights).all()

# UPDATE
def update_flight(db: Session, flight_id: int, flight: FlightCreate) -> FlightResponse:
    db_flight = db.query(Flights).filter(Flights.flight_id == flight_id).first()
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    for key, value in flight.model_dump().items():
        setattr(db_flight, key, value)
    db.commit()
    db.refresh(db_flight)
    return db_flight

# DELETE
def delete_flight(db: Session, flight_id: int):
    db_flight = db.query(Flights).filter(Flights.flight_id == flight_id).first()
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    db.delete(db_flight)
    db.commit()
    return {"message": f"Flight {flight_id} deleted successfully"}
