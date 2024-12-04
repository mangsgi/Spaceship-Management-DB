from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from typing import Optional, List
from datetime import datetime
from operations import administrators, customers, flights, maintenance_records, maintenance_tasks, mechanics, pilot_flights, pilots, reservations, spaceships, user_roles, licenses
from models import (
    PilotCreate, PilotResponse, PilotUpdateRequest,
    FlightCreate, FlightResponse, FlightUpdateRequest,
    SpaceshipCreate, SpaceshipResponse,
    PilotFlightCreate, PilotFlightResponse,
    MaintenanceTaskCreate, MaintenanceTaskResponse, MaintenanceTaskUpdateRequest,
    MaintenanceRecordCreate, MaintenanceRecordResponse, 
    CustomerCreate, CustomerResponse, CustomerUpdateRequest,
    ReservationCreate, ReservationResponse,
    MechanicCreate, MechanicResponse,
    AdministratorCreate, AdministratorResponse, 
    UserRoleCreate, UserRoleResponse,
    LicenseResponse, LicenseCreateRequest
)

app = FastAPI() # API 엔드포인트와 설정을 이 객체에 연결

origins = [ # CORS를 설정하여, 다른 도메인에서의 API 요청을 허용
    # "http://localhost:5000",  # Svelte 기본 포트
    # "http://localhost:3000",  # Svelte 다른 포트 사용 시
    "http://localhost:8080",  # Svelte 다른 포트 사용 시
    # "http://localhost:8000",  # uvicorn 기본 포트
    # 필요에 따라 다른 도메인 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 또는 ["*"]으로 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 테이블 생성 및 초기화
Base.metadata.create_all(bind=engine)

# 의존성: 데이터베이스 세션 생성
def get_db(): # API 엔드포인트에서 데이터베이스 세션을 가져옴
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Database initialized with tables!"}

# ---------------------------------------------------
# Pilots Endpoints
# ---------------------------------------------------

# TODO 삭제

# * - Pliot 생성(면허가 있어야 하나?)
@app.post("/pilots", response_model=PilotResponse)
def create_pilot_endpoint(pilot_data: PilotCreate, db: Session = Depends(get_db)):
    return pilots.create_pilot(db, pilot_data)

# FIN Administrator - 라이선스가 있는 모든 파일럿 조회 -> 비행 일정 생성과 수정 및 파일럿 할당
@app.get("/pilots/available", response_model=List[PilotResponse])
def get_available_pilots_endpoint(
    departure_time: Optional[datetime] = None,
    departure_location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return pilots.get_available_pilots(db, departure_time, departure_location)

# Pilot - 본인의 개인정보 수정
@app.patch("/pilots/{pilot_id}")
def update_pilot_information_endpoint(pilot_id: int, pilot_data: PilotUpdateRequest, db: Session = Depends(get_db)):
    return pilots.update_pilot_information(db, pilot_id, pilot_data)

# ---------------------------------------------------
# Flights Endpoints
# ---------------------------------------------------

# Administrator - 비행 일정 생성
@app.post("/flights", response_model=FlightResponse)
def create_flight_endpoint(flight_data: FlightCreate, db: Session = Depends(get_db)):
    return flights.create_flight(db, flight_data)

# Administrator - 비행 일정 수정
@app.patch("/flights/{flight_id}", response_model=FlightResponse)
def update_flight_endpoint(flight_id: int, flight_data: FlightUpdateRequest, db: Session = Depends(get_db)):
    return flights.update_flight_information(db, flight_id, flight_data)

# Administrator - 비행 일정 삭제
@app.delete("/flights/{flight_id}")
def delete_flight_endpoint(flight_id: int, db: Session = Depends(get_db)):
    return flights.delete_flight(db, flight_id) # return message

# Pilot - 자신에게 할당된 비행 일정 조회 Fin 현재 이후 일정만 조회
@app.get("/pilot_flights/{pilot__id}/{is_current}", response_model=List[PilotFlightResponse])
def read_pilot_flights_endpoint(pilot_id: int, is_current: Optional[bool] = False, db: Session = Depends(get_db)):
    return flights.read_pilot_flights(db, pilot_id, is_current)

# Customer - 비행 일정 조회
@app.get("/flights/search/", response_model=List[FlightResponse])
def get_flights_endpoint(
    departure_location: Optional[str] = None,
    arrival_location: Optional[str] = None,
    departure_date: Optional[str] = None, # 날짜와 시간에서 날짜만 선택 가능
    sort_by: Optional[str] = "departure_time", # 기본값 : 출발 시간 기준 정렬 {departure_date, arrival_time 등 ..}
    db: Session = Depends(get_db)
):
    return flights.get_flights(db, departure_location, arrival_location, departure_date, sort_by)

# Fin Administrator - 조종사가 할당되지 않은 비행 일정 조회 to 조종사 할당
@app.get("/unassigned_flights", response_model=List[FlightResponse])
def get_unassigned_flights_endpoint(db: Session = Depends(get_db)):
    return flights.get_unassigned_flights(db)

# ---------------------------------------------------
# Spaceships Endpoints
# ---------------------------------------------------

# Fin Administrator - 우주선 조회 in order to 비행 일정 생성과 수정 및 우주선 할당
@app.get("/spaceships/available", response_model=List[SpaceshipResponse])
def retrieve_available_spaceships(
    departure_time: Optional[datetime] = None, 
    arrival_time: Optional[datetime] = None, 
    db: Session = Depends(get_db)
):
    return spaceships.get_available_spaceships(db, departure_time, arrival_time)

# Administrator - 우주선 상태 업데이트
@app.patch("/spaceships/{spaceship_id}/status", response_model=MaintenanceTaskResponse) # "운영 중", "점검 중"
def update_spaceship_status_endpoint(spaceship_id: int, update_status = str, db: Session = Depends(get_db)):
    return spaceships.update_spaceship_status(db, spaceship_id, update_status) 

# ---------------------------------------------------
# PilotFlights Endpoints
# ---------------------------------------------------

# Administrator - 조종사 할당
@app.post("/pilot_flights/pilot_assignment/", response_model=PilotFlightResponse)
def assign_pilot_to_flight_endpoint(pilot_flight_data: PilotFlightCreate, db: Session = Depends(get_db)):
    return pilot_flights.assign_pilot_to_flight(db, pilot_flight_data)

# ---------------------------------------------------
# MaintenanceTasks Endpoints
# ---------------------------------------------------

# Administrator - 유지 보수 일정 조회
@app.get("/maintenance_tasks/", response_model=List[MaintenanceTaskResponse])
def read_maintenance_tasks_endpoint(
    task_type: Optional[str] = None, 
    priority: Optional[int] = None, 
    deadline: Optional[str] = None, 
    db: Session = Depends(get_db)):
    return maintenance_tasks.get_maintenance_tasks(db, task_type, priority, deadline)

# Fin Mechanic - 본인이 할당된 유지 보수 작업 조회
@app.get("/maintenance_tasks/mechanic/{mechanic_id}", response_model=List[MaintenanceTaskResponse])
def read_maintenance_tasks_for_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    return maintenance_tasks.get_maintenance_tasks_by_mechanic(db, mechanic_id)

# Administrator - 유지 보수 일정 생성
@app.post("/maintenance_tasks/", response_model=MaintenanceTaskResponse)
def create_maintenance_task_endpoint(task_data: MaintenanceTaskCreate, db: Session = Depends(get_db)):
    return maintenance_tasks.create_maintenance_task(db, task_data)

# Administrator - 유지 보수 일정 조회
@app.get("/maintenance_tasks_all/", response_model=List[MaintenanceTaskResponse])
def get_maintenance_tasks_endpoint(spaceship_id: Optional[int] = None, db: Session = Depends(get_db)):
    return maintenance_tasks.get_maintenance_tasks(db, spaceship_id)

# Administrator - 유지 보수 일정 수정
@app.patch("/maintenance_tasks/{task_id}", response_model=MaintenanceTaskResponse)
def update_maintenance_task_endpoint(task_id: int, task_data: MaintenanceTaskUpdateRequest, db: Session = Depends(get_db)):
    return maintenance_tasks.update_maintenance_task(db, task_id, task_data)

# ---------------------------------------------------
# MaintenanceRecords Endpoints
# ---------------------------------------------------

# Mechanic - 유지 보수 작업 기록하기
@app.post("/maintenance_records/", response_model=MaintenanceRecordResponse)
def create_maintenance_record_endpoint(record: MaintenanceRecordCreate, db: Session = Depends(get_db)):
    return maintenance_records.create_maintenance_record(db, record)

# ---------------------------------------------------
# Customers Endpoints
# ---------------------------------------------------

# TODO Customer 조회 삭제

# * - 고객 생성
@app.post("/customers", response_model=dict)
def create_customer_endpoint(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    return customers.create_customer(db, customer_data)

# Customers - 본인의 개인정보 수정
@app.patch("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer_information_endpoint(customer_id: int, customer_data: CustomerUpdateRequest, db: Session = Depends(get_db)):
    return customers.update_customer_information(db, customer_id, customer_data)

# ---------------------------------------------------
# Reservations Endpoints
# ---------------------------------------------------

# Customer - 좌석 예약
@app.post("/reservations/", response_model=ReservationResponse)
def reserve_flight_seat_endpoint(reservation_data: ReservationCreate, db: Session = Depends(get_db)):
    return reservations.reserve_flight_seat(db, reservation_data)

# Customer - 예약 조회
@app.get("/reservations/my", response_model=List[ReservationResponse])
def get_reservations_endpoint(
    customer_id: int,
    status: Optional[str] = None,
    reservation_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return reservations.get_customer_reservations(db, customer_id, status, reservation_date)

# Customer - 예약 취소
@app.patch("/reservations/my/cancel/{reservation_id}")
def cancel_reservation_endpoint(customer_id: int, reservation_id: int, db: Session = Depends(get_db)):
    return reservations.cancel_customer_reservation(db, customer_id, reservation_id) # dictionary 리턴

# ---------------------------------------------------
# Mechanics Endpoints
# ---------------------------------------------------

# Fin 정비사 조회(id가 주어지면 해당 정비사만 조회)
@app.get("/mechanics", response_model=list[MechanicResponse])
def get_mechanics_endpoint(mechanic_id: Optional[int] = None, db: Session = Depends(get_db)):
    return mechanics.get_mechanics(db, mechanic_id)

# TODO 정비사 삭제, 업데이트

# * - 정비사 생성
@app.post("/mechanics", response_model=dict)
def create_mechanic_endpoint(mechanic_data: MechanicCreate, db: Session = Depends(get_db)):
    return mechanics.create_mechanic(db, mechanic_data)

# ---------------------------------------------------
# Administrators Endpoints
# ---------------------------------------------------

# TODO 관리자 생성, 조회, 삭제, 업데이트 필요

# * - 관리자 생성
@app.post("/administrators", response_model=dict)
def create_administrator_endpoint(admin_data: AdministratorCreate, db: Session = Depends(get_db)):
    return administrators.create_administrator(db, admin_data)

# ---------------------------------------------------
# UserRoles Endpoints
# ---------------------------------------------------

# Fin * - Pilots Customers Administrators Mechanics 연결해서 회원 만들어질 때마다 추가

# ---------------------------------------------------
# Licenses Endpoints
# ---------------------------------------------------

# Pilot - 파일럿의 새로운 라이선스 추가 (PDF 포함)
@app.post("/pilots/{pilot_id}/licenses", response_model=LicenseResponse)
def add_license_endpoint(pilot_id: int, license_data: LicenseCreateRequest = Depends(), license_file: UploadFile = File(...), db: Session = Depends(get_db)):
    return licenses.add_license(db, pilot_id, license_data, license_file)

# Administartor - 라이선스 상태 변경
@app.patch("/licenses/{license_id}/status", response_model=LicenseResponse)
def update_license_status_endpoint(license_id: int, new_status: str, db: Session = Depends(get_db)):
    return licenses.update_license_status(db, license_id, new_status) # 허가, 갱신 중, 만료

# TODO License 정보 조회 (PDF 포함)