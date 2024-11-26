from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from operations import (
    create_pilot, get_all_pilots, update_pilot, delete_pilot,
    create_flight, get_all_flights, update_flight, delete_flight,
    create_spaceship, get_all_spaceships, update_spaceship, delete_spaceship,
    create_pilot_flight, get_all_pilot_flights, update_pilot_flight, delete_pilot_flight,
    create_customer, get_all_customers, update_customer, delete_customer,
    create_maintenance_task, get_all_maintenance_tasks, update_maintenance_task, delete_maintenance_task,
    create_maintenance_record, get_all_maintenance_records, update_maintenance_record, delete_maintenance_record,
    create_reservation, get_all_reservations, update_reservation, delete_reservation,
    create_mechanic, get_all_mechanics, update_mechanic, delete_mechanic,
    create_administrator, get_all_administrators, update_administrator, delete_administrator
)

from models import (
    PilotCreate, PilotResponse,
    FlightCreate, FlightResponse,
    SpaceshipCreate, SpaceshipResponse,
    PilotFlightCreate, PilotFlightResponse,
    MaintenanceTaskCreate, MaintenanceTaskResponse,
    MaintenanceRecordCreate, MaintenanceRecordResponse,
    CustomerCreate, CustomerResponse,
    ReservationCreate, ReservationResponse,
    MechanicCreate, MechanicResponse,
    AdministratorCreate, AdministratorResponse, 
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

@app.post("/pilots/", response_model=PilotResponse)
def create_pilot_endpoint(pilot: PilotCreate, db: Session = Depends(get_db)):
    return create_pilot(db, pilot)

@app.get("/pilots/", response_model=list[PilotResponse])
def read_all_pilots_endpoint(db: Session = Depends(get_db)):
    return get_all_pilots(db)

@app.put("/pilots/{pilot_id}", response_model=PilotResponse)
def update_pilot_endpoint(pilot_id: int, pilot: PilotCreate, db: Session = Depends(get_db)):
    return update_pilot(db, pilot_id, pilot)

@app.delete("/pilots/{pilot_id}")
def delete_pilot_endpoint(pilot_id: int, db: Session = Depends(get_db)):
    return delete_pilot(db, pilot_id)

# ---------------------------------------------------
# Flights Endpoints
# ---------------------------------------------------

@app.post("/flights/", response_model=FlightResponse)
def create_flight_endpoint(flight: FlightCreate, db: Session = Depends(get_db)):
    return create_flight(db, flight)

@app.get("/flights/", response_model=list[FlightResponse])
def read_all_flights_endpoint(db: Session = Depends(get_db)):
    return get_all_flights(db)

@app.put("/flights/{flight_id}", response_model=FlightResponse)
def update_flight_endpoint(flight_id: int, flight: FlightCreate, db: Session = Depends(get_db)):
    return update_flight(db, flight_id, flight)

@app.delete("/flights/{flight_id}")
def delete_flight_endpoint(flight_id: int, db: Session = Depends(get_db)):
    return delete_flight(db, flight_id)

# ---------------------------------------------------
# Spaceships Endpoints
# ---------------------------------------------------

@app.post("/spaceships/", response_model=SpaceshipResponse)
def create_spaceship_endpoint(spaceship: SpaceshipCreate, db: Session = Depends(get_db)):
    return create_spaceship(db, spaceship)

@app.get("/spaceships/", response_model=list[SpaceshipResponse])
def read_all_spaceships_endpoint(db: Session = Depends(get_db)):
    return get_all_spaceships(db)

@app.put("/spaceships/{spaceship_id}", response_model=SpaceshipResponse)
def update_spaceship_endpoint(spaceship_id: int, spaceship: SpaceshipCreate, db: Session = Depends(get_db)):
    return update_spaceship(db, spaceship_id, spaceship)

@app.delete("/spaceships/{spaceship_id}")
def delete_spaceship_endpoint(spaceship_id: int, db: Session = Depends(get_db)):
    return delete_spaceship(db, spaceship_id)

# ---------------------------------------------------
# PilotFlights Endpoints
# ---------------------------------------------------

@app.post("/pilot_flights/", response_model=PilotFlightResponse)
def create_pilot_flight_endpoint(pilot_flight: PilotFlightCreate, db: Session = Depends(get_db)):
    return create_pilot_flight(db, pilot_flight)

@app.get("/pilot_flights/", response_model=list[PilotFlightResponse])
def read_all_pilot_flights_endpoint(db: Session = Depends(get_db)):
    return get_all_pilot_flights(db)

@app.put("/pilot_flights/{pilot_flight_id}", response_model=PilotFlightResponse)
def update_pilot_flight_endpoint(pilot_flight_id: int, pilot_flight: PilotFlightCreate, db: Session = Depends(get_db)):
    return update_pilot_flight(db, pilot_flight_id, pilot_flight)

@app.delete("/pilot_flights/{pilot_flight_id}")
def delete_pilot_flight_endpoint(pilot_flight_id: int, db: Session = Depends(get_db)):
    return delete_pilot_flight(db, pilot_flight_id)

# ---------------------------------------------------
# MaintenanceTasks Endpoints
# ---------------------------------------------------

@app.post("/maintenance_tasks/", response_model=MaintenanceTaskResponse)
def create_maintenance_task_endpoint(task: MaintenanceTaskCreate, db: Session = Depends(get_db)):
    return create_maintenance_task(db, task)

@app.get("/maintenance_tasks/", response_model=list[MaintenanceTaskResponse])
def read_all_maintenance_tasks_endpoint(db: Session = Depends(get_db)):
    return get_all_maintenance_tasks(db)

@app.put("/maintenance_tasks/{task_id}", response_model=MaintenanceTaskResponse)
def update_maintenance_task_endpoint(task_id: int, task: MaintenanceTaskCreate, db: Session = Depends(get_db)):
    return update_maintenance_task(db, task_id, task)

@app.delete("/maintenance_tasks/{task_id}")
def delete_maintenance_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    return delete_maintenance_task(db, task_id)

# ---------------------------------------------------
# MaintenanceRecords Endpoints
# ---------------------------------------------------

@app.post("/maintenance_records/", response_model=MaintenanceRecordResponse)
def create_maintenance_record_endpoint(record: MaintenanceRecordCreate, db: Session = Depends(get_db)):
    return create_maintenance_record(db, record)

@app.get("/maintenance_records/", response_model=list[MaintenanceRecordResponse])
def read_all_maintenance_records_endpoint(db: Session = Depends(get_db)):
    return get_all_maintenance_records(db)

@app.put("/maintenance_records/{record_id}", response_model=MaintenanceRecordResponse)
def update_maintenance_record_endpoint(record_id: int, record: MaintenanceRecordCreate, db: Session = Depends(get_db)):
    return update_maintenance_record(db, record_id, record)

@app.delete("/maintenance_records/{record_id}")
def delete_maintenance_record_endpoint(record_id: int, db: Session = Depends(get_db)):
    return delete_maintenance_record(db, record_id)

# ---------------------------------------------------
# Customers Endpoints
# ---------------------------------------------------

@app.post("/customers/", response_model=CustomerResponse)
def create_customer_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)

@app.get("/customers/", response_model=list[CustomerResponse])
def read_all_customers_endpoint(db: Session = Depends(get_db)):
    return get_all_customers(db)

@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    return update_customer(db, customer_id, customer)

@app.delete("/customers/{customer_id}")
def delete_customer_endpoint(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(db, customer_id)

# ---------------------------------------------------
# Reservations Endpoints
# ---------------------------------------------------

@app.post("/reservations/", response_model=ReservationResponse)
def create_reservation_endpoint(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return create_reservation(db, reservation)

@app.get("/reservations/", response_model=list[ReservationResponse])
def read_all_reservations_endpoint(db: Session = Depends(get_db)):
    return get_all_reservations(db)

@app.put("/reservations/{reservation_id}", response_model=ReservationResponse)
def update_reservation_endpoint(reservation_id: int, reservation: ReservationCreate, db: Session = Depends(get_db)):
    return update_reservation(db, reservation_id, reservation)

@app.delete("/reservations/{reservation_id}")
def delete_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    return delete_reservation(db, reservation_id)

# ---------------------------------------------------
# Mechanics Endpoints
# ---------------------------------------------------

@app.post("/mechanics/", response_model=MechanicResponse)
def create_mechanic_endpoint(mechanic: MechanicCreate, db: Session = Depends(get_db)):
    return create_mechanic(db, mechanic)

@app.get("/mechanics/", response_model=list[MechanicResponse])
def read_all_mechanics_endpoint(db: Session = Depends(get_db)):
    return get_all_mechanics(db)

@app.put("/mechanics/{mechanic_id}", response_model=MechanicResponse)
def update_mechanic_endpoint(mechanic_id: int, mechanic: MechanicCreate, db: Session = Depends(get_db)):
    return update_mechanic(db, mechanic_id, mechanic)

@app.delete("/mechanics/{mechanic_id}")
def delete_mechanic_endpoint(mechanic_id: int, db: Session = Depends(get_db)):
    return delete_mechanic(db, mechanic_id)

# ---------------------------------------------------
# Administrators Endpoints
# ---------------------------------------------------

@app.post("/administrators/", response_model=AdministratorResponse)
def create_administrator_endpoint(administrator: AdministratorCreate, db: Session = Depends(get_db)):
    return create_administrator(db, administrator)

@app.get("/administrators/", response_model=list[AdministratorResponse])
def read_all_administrators_endpoint(db: Session = Depends(get_db)):
    return get_all_administrators(db)

@app.put("/administrators/{admin_id}", response_model=AdministratorResponse)
def update_administrator_endpoint(admin_id: int, administrator: AdministratorCreate, db: Session = Depends(get_db)):
    return update_administrator(db, admin_id, administrator)

@app.delete("/administrators/{admin_id}")
def delete_administrator_endpoint(admin_id: int, db: Session = Depends(get_db)):
    return delete_administrator(db, admin_id)