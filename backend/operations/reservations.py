from sqlalchemy.orm import Session
from models import Reservations, ReservationCreate, ReservationResponse
from fastapi import HTTPException

# CREATE
def create_reservation(db: Session, reservation: ReservationCreate) -> ReservationResponse:
    db_reservation = Reservations(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# READ ALL
def get_all_reservations(db: Session) -> list[ReservationResponse]:
    return db.query(Reservations).all()

# UPDATE
def update_reservation(db: Session, reservation_id: int, reservation: ReservationCreate) -> ReservationResponse:
    db_reservation = db.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.model_dump().items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# DELETE
def delete_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return {"message": f"Reservation {reservation_id} deleted successfully"}
