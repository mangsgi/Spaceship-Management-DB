from sqlalchemy.orm import Session
from models import PilotFlights, PilotFlightCreate, PilotFlightResponse
from fastapi import HTTPException

# CREATE
def create_pilot_flight(db: Session, pilot_flight: PilotFlightCreate) -> PilotFlightResponse:
    db_pilot_flight = PilotFlights(**pilot_flight.model_dump())
    db.add(db_pilot_flight)
    db.commit()
    db.refresh(db_pilot_flight)
    return db_pilot_flight

# READ ALL
def get_all_pilot_flights(db: Session) -> list[PilotFlightResponse]:
    return db.query(PilotFlights).all()

# UPDATE
def update_pilot_flight(db: Session, pilot_flight_id: int, pilot_flight: PilotFlightCreate) -> PilotFlightResponse:
    db_pilot_flight = db.query(PilotFlights).filter(PilotFlights.pilot_flight_id == pilot_flight_id).first()
    if not db_pilot_flight:
        raise HTTPException(status_code=404, detail="Pilot Flight not found")
    for key, value in pilot_flight.model_dump().items():
        setattr(db_pilot_flight, key, value)
    db.commit()
    db.refresh(db_pilot_flight)
    return db_pilot_flight

# DELETE
def delete_pilot_flight(db: Session, pilot_flight_id: int):
    db_pilot_flight = db.query(PilotFlights).filter(PilotFlights.pilot_flight_id == pilot_flight_id).first()
    if not db_pilot_flight:
        raise HTTPException(status_code=404, detail="Pilot Flight not found")
    db.delete(db_pilot_flight)
    db.commit()
    return {"message": f"Pilot Flight {pilot_flight_id} deleted successfully"}
