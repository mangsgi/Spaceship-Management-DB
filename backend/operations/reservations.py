from sqlalchemy.orm import Session
from models import Reservations, ReservationCreate, ReservationResponse
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Date

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

# Custormer - 좌석 예약
def reserve_seat(
    db: Session,
    customer_id: int,
    flight_id: int,
    seat_number: str
) -> ReservationResponse:
    try:
        # 이미 예약된 좌석인지 확인
        existing_reservation = (
            db.query(Reservations)
            .filter(
                Reservations.flight_id == flight_id,
                Reservations.seat_number == seat_number
            )
            .first()
        )
        if existing_reservation: 
            raise HTTPException(status_code=400, detail=f"Seat {seat_number} on flight {flight_id} is already reserved.")

        # 예약 진행
        new_reservation = Reservations(
            customer_id=customer_id,
            flight_id=flight_id,
            seat_number=seat_number,
            status="예약",
            reservation_date=datetime.now()
        )
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)

        return ReservationResponse.model_validate(new_reservation)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to reserve the seat. Please try again.")
    
# Customer - 예약 조회
def get_customer_reservations(
    db: Session,
    customer_id: int,
    status: Optional[str] = None,
    reservation_date: Optional[str] = None
) -> List[ReservationResponse]:
    query = db.query(Reservations).filter(Reservations.customer_id == customer_id)

    # 상태로 필터링
    if status:
        query = query.filter(Reservations.status == status)

    # 예약 날짜로 필터링
    if reservation_date:
        query = query.filter(Reservations.reservation_date.cast(Date) == reservation_date)

    reservations = query.all()
    if not reservations:
        return []
    return [ReservationResponse.model_validate(reservation) for reservation in reservations]

# Customer - 예약 취소
def cancel_customer_reservation(
    db: Session,
    customer_id: int,
    reservation_id: int
) -> dict:
    try:
        # 특정 사용자의 예약 검색
        reservation = (
            db.query(Reservations)
            .filter(
                Reservations.customer_id == customer_id,
                Reservations.reservation_id == reservation_id
            )
            .first()
        )

        # 예약이 없을 경우 처리
        if not reservation:
            return HTTPException(status_code=400, detail="예약을 찾을 수 없습니다.")

        # 이미 취소된 예약 처리
        if reservation.status == "취소":
            return HTTPException(status_code=401, detail="이미 취소된 예약입니다.")

        # 예약 상태를 '취소'로 업데이트
        reservation.status = "취소"
        db.commit()
        return {"message": f"예약 ID {reservation_id}가 성공적으로 취소되었습니다."} # 딱히 return할 건 없으니까

    except Exception as e:
        db.rollback()
        return HTTPException(status_code=402, detail=f"예약 취소 중 오류가 발생했습니다: {str(e)}")