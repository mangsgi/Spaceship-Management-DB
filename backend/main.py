from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from typing import Optional, List
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

# TODO Pliot 생성 조회 삭제

# Pilot - 본인의 개인정보 수정
@app.patch("/pilots/{pilot_id}")
def update_pilot_information_endpoint(pilot_id: int, pilot_data: PilotUpdateRequest, db: Session = Depends(get_db)):
    return pilots.update_pilot_information(db, pilot_id, pilot_data)

# ---------------------------------------------------
# Flights Endpoints
# ---------------------------------------------------

# Customer - 비행 일정 조회
@app.get("/flights/search/", response_model=List[FlightResponse])
def get_flights(
    departure_location: Optional[str] = None,
    arrival_location: Optional[str] = None,
    departure_date: Optional[str] = None, # 날짜와 시간에서 날짜만 선택 가능
    sort_by: Optional[str] = "departure_time", # 기본값 : 출발 시간 기준 정렬 {departure_date, arrival_time 등 ..}
    db: Session = Depends(get_db)
):
    return flights.search_flights(db, departure_location, arrival_location, departure_date, sort_by)

# Administrator - 비행 일정 생성 TODO 이미 그 우주선이 사용 중이라면?
@app.post("/flights", response_model=FlightResponse)
def create_flight_endpoint(flight_data: FlightCreate, db: Session = Depends(get_db)):
    return flights.create_flight(db, flight_data)

# Administrator - 비행 일정 수정 TODO 이미 그 우주선이 사용 중이라면?
@app.patch("/flights/{flight_id}", response_model=FlightResponse)
def update_flight_endpoint(flight_id: int, flight_data: FlightUpdateRequest, db: Session = Depends(get_db)):
    return flights.update_flight_information(db, flight_id, flight_data)

# Administrator - 비행 일정 삭제
@app.delete("/flights/{flight_id}")
def delete_flight_endpoint(flight_id: int, db: Session = Depends(get_db)):
    return flights.delete_flight(db, flight_id) # return message

# ---------------------------------------------------
# Spaceships Endpoints
# ---------------------------------------------------

# Administrator - 우주선 상태 업데이트
@app.patch("/spaceships/{spaceship_id}/status", response_model=MaintenanceTaskResponse) # "운영 중", "점검 중"
def update_spaceship_status_endpoint(spaceship_id: int, update_status = str, db: Session = Depends(get_db)):
    return spaceships.update_spaceship_status(db, spaceship_id, update_status) 

# ---------------------------------------------------
# PilotFlights Endpoints
# ---------------------------------------------------

# Pilot - 자신에게 할당된 비행 일정 조회, TODO 현재 진행중인 것만 볼 수 있도록 선택하는 방향으로 하려면.. 추가해야 함.
@app.get("/pilot_flights/{pilot__id}", response_model=list[PilotFlightResponse])
def read_pilot_flights_endpoint(pilot_id: int, db: Session = Depends(get_db)):
    return pilot_flights.read_pilot_flights(db, pilot_id)

# Administrator - 조종사 할당, TODO Pliots(면허 있는) 쭈루룩 조회랑 Flights 쭈루룩(조종사 할당 안된) 조회 기능 필요
@app.post("/pilot_flights/pilot_assignment/", response_model=PilotFlightResponse)
def assign_pilot_to_flight_endpoint(pilot_flight_data: PilotFlightCreate, db: Session = Depends(get_db)):
    return pilot_flights.assign_pilot_to_flight(db, pilot_flight_data)

# ---------------------------------------------------
# MaintenanceTasks Endpoints
# ---------------------------------------------------

# Mechanic - 유지 보수 작업 할당 조회, TODO 맡은 tasks만 볼 수 있도록 하려면.. 엄청 만들어야 함..
@app.get("/maintenance_tasks/", response_model=list[MaintenanceTaskResponse])
def read_maintenance_tasks(
    task_type: Optional[str] = None, 
    priority: Optional[int] = None, 
    deadline: Optional[str] = None, 
    db: Session = Depends(get_db)):
    return maintenance_tasks.get_maintenance_tasks(db, task_type, priority, deadline)

# Administrator - 유지 보수 일정 생성
@app.post("/maintenance_tasks/", response_model=MaintenanceTaskResponse)
def create_maintenance_task_endpoint(task_data: MaintenanceTaskCreate, db: Session = Depends(get_db)):
    return maintenance_tasks.create_maintenance_task(db, task_data)

# Administrator - 유지 보수 일정 조회
@app.get("/maintenance_tasks_all/", response_model=list[MaintenanceTaskResponse])
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
def get_reservations(
    customer_id: int,
    status: Optional[str] = None,
    reservation_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    my_reservations = reservations.get_customer_reservations(db, customer_id, status, reservation_date)
    if not my_reservations:
        return []
    return my_reservations

# Customer - 예약 취소
@app.patch("/reservations/my/cancel/{reservation_id}")
def cancel_reservation(customer_id: int, reservation_id: int, db: Session = Depends(get_db)):
    return reservations.cancel_customer_reservation(db, customer_id, reservation_id) # dictionary 리턴

# ---------------------------------------------------
# Mechanics Endpoints
# ---------------------------------------------------

# TODO 정비사 생성, 조회, 삭제, 업데이트 필요

# ---------------------------------------------------
# Administrators Endpoints
# ---------------------------------------------------

# TODO 관리자 생성, 조회, 삭제, 업데이트 필요

# ---------------------------------------------------
# UserRoles Endpoints
# ---------------------------------------------------

# TODO Pilots Customers Administrators Mechanics 연결해서 회원 만들어질 때마다 더해지도록 하기.

# ---------------------------------------------------
# Licenses Endpoints
# ---------------------------------------------------

# Pilot - 파일럿의 새로운 라이선스 추가 (PDF 포함) TODO Pilot이 등록될 때 면허가 있어야 되지 않을까?
@app.post("/pilots/{pilot_id}/licenses", response_model=LicenseResponse)
def add_license_endpoint(pilot_id: int, license_data: LicenseCreateRequest = Depends(), license_file: UploadFile = File(...), db: Session = Depends(get_db)):
    return licenses.add_license(db, pilot_id, license_data, license_file)

# 라이선스 상태 변경 TODO 아마 Administartor가 할 수 있도록 해야겠지
@app.patch("/licenses/{license_id}/status", response_model=LicenseResponse)
def update_license_status_endpoint(license_id: int, new_status: str, db: Session = Depends(get_db)):
    return licenses.update_license_status(db, license_id, new_status) # 허가, 갱신 중, 만료

# TODO License 정보 조회 (PDF 포함)