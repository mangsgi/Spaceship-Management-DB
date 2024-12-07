from sqlalchemy.orm import Session
from models import Reservations, ReservationCreate, ReservationResponse, Flights, ReservationUpdateRequest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Date

# Custormer - 좌석 예약
def reserve_flight_seat(db: Session, reservation_data: ReservationCreate) -> ReservationResponse:
    try:
        # 존재하는 Flights인지 확인
        flight_exists = db.query(Flights).filter(Flights.flight_id == reservation_data.flight_id).first()
        if not flight_exists:
            raise HTTPException(status_code=402, detail=f"비행기 ID {reservation_data.flight_id}를 찾을 수 없습니다.")
 
        # 이미 예약된 좌석인지 확인
        existing_reservation = (
            db.query(Reservations)
            .filter(
                Reservations.flight_id == reservation_data.flight_id,
                Reservations.seat_number == reservation_data.seat_number,
                Reservations.status == "예약"
            )
            .first()
        )
        if existing_reservation: 
            raise HTTPException(status_code=400, detail=f"비행기 {reservation_data.flight_id}의 {reservation_data.seat_number}이 이미 예약된 좌석입니다.")

        # 예약 진행
        new_reservation = Reservations(
            customer_id = reservation_data.customer_id,
            flight_id = reservation_data.flight_id,
            seat_number = reservation_data.seat_number,
            status = "예약",
            reservation_date = datetime.now().replace(second=0, microsecond=0)
        )
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)

        return ReservationResponse.model_validate(new_reservation)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=401, detail="좌석 예약에 실패했습니다. 다시 시도해주세요.")
    
# Customer - 예약 조회
def get_customer_reservations(
    db: Session,
    customer_id: int,
    status: Optional[str] = None,
    reservation_date: Optional[date] = None
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
def cancel_customer_reservation(db: Session, customer_data: ReservationUpdateRequest, reservation_id: int) -> dict:
    try:
        # 특정 사용자의 예약 검색
        reservation = (
            db.query(Reservations)
            .filter(
                Reservations.customer_id == customer_data.customer_id,
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
        return ReservationResponse.model_validate(reservation) # 딱히 return할 건 없음.

    except Exception as e:
        db.rollback()
        return HTTPException(status_code=402, detail=f"예약 취소 중 오류가 발생했습니다: {str(e)}")