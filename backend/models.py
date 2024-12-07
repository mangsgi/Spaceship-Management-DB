from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Float, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

'''
데이터베이스 테이블 정의
'''

class Pilots(Base): # 조종사 테이블
    __tablename__ = "pilots" # pilots 클래스를 pilots table에 매핑
    pilot_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)
    emergency_contact = Column(String)

    licenses = relationship("Licenses", back_populates="pilot")  # 라이선스와 관계 설정
    user_role = relationship("UserRoles", back_populates="pilot")  # 역할 관계 설정


class Flights(Base): # 비행편 테이블
    __tablename__ = "flights"
    flight_id = Column(Integer, primary_key=True, index=True)
    spaceship_id = Column(Integer, ForeignKey("spaceships.spaceship_id", ondelete="CASCADE"), nullable=False)
    departure_location = Column(String, nullable=False)
    arrival_location = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    status = Column(Enum("예정", "진행 중", "완료", name="flight_status"), nullable=False)

    spaceship = relationship("Spaceships", back_populates="flights") # 두 테이블 간의 관계를 정의, back_populates로 양방향 관계를 설정, Flights에서 Spaceships 참조

class Spaceships(Base): # 우주선 테이블
    __tablename__ = "spaceships"
    spaceship_id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    manufacture_date = Column(Date, nullable=False)
    status = Column(Enum("운영 중", "점검 중", name="spaceship_status"), nullable=False)

    flights = relationship("Flights", back_populates="spaceship")
    maintenance_tasks = relationship("MaintenanceTasks", back_populates="spaceship")

class PilotFlights(Base): # 조종사 비행 일정 테이블
    __tablename__ = "pilot_flights"
    pilot_flight_id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.flight_id", ondelete="CASCADE"), nullable=False)
    pilot_id = Column(Integer, ForeignKey("pilots.pilot_id", ondelete="CASCADE"), nullable=False)

class MaintenanceTasks(Base):  # 우주선 유지보수 테이블
    __tablename__ = "maintenance_tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    spaceship_id = Column(Integer, ForeignKey("spaceships.spaceship_id", ondelete="CASCADE"), nullable=False)
    task_type = Column(Enum("정기 점검", "수리", name="task_type"), nullable=False)
    priority = Column(Integer, nullable=False)
    deadline = Column(Date, nullable=False)
    status = Column(Enum("대기 중", "완료", "진행 중", name="task_status"), nullable=False)

    spaceship = relationship("Spaceships", back_populates="maintenance_tasks")
    maintenance_records = relationship("MaintenanceRecords", back_populates="maintenance_task")
    assigned_mechanics = relationship("Mechanics", secondary="maintenance_task_assignments", back_populates="assigned_tasks",)

class MaintenanceTaskAssignments(Base): # 정비사와 유지보수 작업의 다대다 관계를 위한 중간 테이블
    __tablename__ = "maintenance_task_assignments"
    assignment_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("maintenance_tasks.task_id", ondelete="CASCADE"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id", ondelete="CASCADE"), nullable=False)

class Mechanics(Base):  # 정비사 테이블
    __tablename__ = "mechanics"
    mechanic_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)

    assigned_tasks = relationship("MaintenanceTasks", secondary="maintenance_task_assignments", back_populates="assigned_mechanics",)
    user_role = relationship("UserRoles", back_populates="mechanic")  # 역할 관계 설정

class MaintenanceRecords(Base): # 유지보수 기록 테이블
    __tablename__ = "maintenance_records"
    record_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("maintenance_tasks.task_id", ondelete="CASCADE"), nullable=False)
    details = Column(String)
    parts_used = Column(String)
    time_spent = Column(Float)

    maintenance_task = relationship("MaintenanceTasks", back_populates="maintenance_records")

class Customers(Base): # 승객 테이블
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)

    user_role = relationship("UserRoles", back_populates="customer")  # 역할 관계 설정

class Reservations(Base): # 예약 테이블
    __tablename__ = "reservations"
    reservation_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.flight_id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(String, nullable=False)
    status = Column(Enum("예약", "취소", name="reservation_status"), nullable=False)
    reservation_date = Column(DateTime, nullable=False)

class UserRoles(Base):  # 역할 테이블
    __tablename__ = "user_roles"
    user_role_id = Column(Integer, primary_key=True, index=True)
    pilot_id = Column(Integer, ForeignKey("pilots.pilot_id", ondelete="CASCADE"), nullable=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id", ondelete="CASCADE"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=True)
    admin_id = Column(Integer, ForeignKey("administrators.admin_id", ondelete="CASCADE"), nullable=True)
    role = Column(Enum("관리자", "조종사", "정비사", "고객", name="user_role"), nullable=False)

    pilot = relationship("Pilots", back_populates="user_role")
    mechanic = relationship("Mechanics", back_populates="user_role")
    customer = relationship("Customers", back_populates="user_role")
    admin = relationship("Administrators", back_populates="user_role")


class Administrators(Base): # 관리자 테이블
    __tablename__ = "administrators"
    admin_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    role = Column(String, nullable=False)

    user_role = relationship("UserRoles", back_populates="admin")  # 역할 관계 설정

class Licenses(Base):  # 라이선스 테이블
    __tablename__ = "licenses"
    license_id = Column(Integer, primary_key=True, index=True)  # Primary Key가 필수여서..
    pilot_id = Column(Integer, ForeignKey("pilots.pilot_id", ondelete="CASCADE"), nullable=False)
    license_status = Column(Enum("허가", "갱신 중", "만료", name="license_status"), nullable=False)
    license_number = Column(String, nullable=False)
    license_expiry_date = Column(Date, nullable=False)
    license_document = Column(LargeBinary, nullable=True)  # PDF 파일 저장

    pilot = relationship("Pilots", back_populates="licenses") 

'''
Pydantic 모델 정의
API 요청 시 데이터를 검증하고 구조화
'''

# Pilots
class PilotCreate(BaseModel): # 새 Pilot을 생성할 때 사용하는 Request 모델
    name: str
    contact_info: str
    emergency_contact: str

class PilotResponse(BaseModel): # 데이터베이스 ORM 객체를 반환할 때 사용하는 Response 모델
    pilot_id: int
    name: str
    contact_info: str
    emergency_contact: str

    class Config: # Config 설정
        from_attributes = True # SQLAlchemy ORM 객체를 Pydantic 모델로 변환할 때 사용

class PilotUpdateRequest(BaseModel): # 파일럿 개인정보 수정용 테이블
    name: Optional[str] = None
    contact_info: Optional[str] = None
    emergency_contact: Optional[str] = None

# Flights
class FlightCreate(BaseModel):
    spaceship_id: int
    departure_location: str
    arrival_location: str
    departure_time: datetime
    arrival_time: datetime
    status: str

class FlightResponse(BaseModel):
    flight_id: int
    spaceship_id: int
    departure_location: str
    arrival_location: str
    departure_time: datetime 
    arrival_time: datetime
    status: str

    class Config:
        from_attributes = True

class FlightUpdateRequest(BaseModel): # 비행 일정 수정용 테이블
    departure_location: Optional[str] = None
    arrival_location: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    status: Optional[str] = None
    
# Spaceships
class SpaceshipCreate(BaseModel):
    model: str
    manufacture_date: date
    status: str

class SpaceshipResponse(BaseModel):
    spaceship_id: int
    model: str
    manufacture_date: date
    status: str

    class Config:
        from_attributes = True

class SpaceshipUpdateRequest(BaseModel): # 우주선 상태 수정용 테이블
    status: str

# PilotFlights
class PilotFlightCreate(BaseModel):
    flight_id: int
    pilot_id: int

class PilotFlightResponse(BaseModel):
    pilot_flight_id: int
    flight_id: int
    pilot_id: int

    class Config:
        from_attributes = True

class PilotFlightScheduleResponse(BaseModel): # 일단 보류
    pilot: PilotCreate
    flights: List[dict]  # Contains details of flights the pilot is assigned to

    class Config:
        from_attributes = True

# MaintenanceTasks
class MaintenanceTaskCreate(BaseModel):
    spaceship_id: int
    task_type: str
    priority: int
    deadline: date
    status: str

class MaintenanceTaskResponse(BaseModel):
    task_id: int
    spaceship_id: int
    task_type: str
    priority: int
    deadline: date
    status: str
    assigned_mechanics: List[int]
    
    class Config:
        from_attributes = True

class MaintenanceTaskUpdateRequest(BaseModel): # 유지 보수 일정 수정용 테이블
    task_type: Optional[str] = None
    priority: Optional[int] = None
    deadline: Optional[date] = None
    status: Optional[str] = None
    assigned_mechanics: Optional[List[int]] = None

# MaintenanceRecords
class MaintenanceRecordCreate(BaseModel):
    task_id: int
    details: Optional[str] = None
    parts_used: Optional[str] = None
    time_spent: Optional[float] = None

class MaintenanceRecordResponse(BaseModel):
    record_id: int
    task_id: int
    details: Optional[str]
    parts_used: Optional[str]
    time_spent: Optional[float]

    class Config:
        from_attributes = True

# Customers
class CustomerCreate(BaseModel):
    name: str
    contact_info: str

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    contact_info: str

    class Config:
        from_attributes = True

class CustomerUpdateRequest(BaseModel): # 고객 개인정보 수정용 테이블
    name: Optional[str] = None
    contact_info: Optional[str] = None

# Reservations
class ReservationCreate(BaseModel):
    customer_id: int
    flight_id: int
    seat_number: str

class ReservationResponse(BaseModel):
    reservation_id: int
    customer_id: int
    flight_id: int
    seat_number: str
    status: str
    reservation_date: datetime

    class Config:
        from_attributes = True

class ReservationUpdateRequest(BaseModel): # 예약 취소용 테이블
    customer_id: int

# Mechanics
class MechanicCreate(BaseModel):
    name: str
    contact_info: str

class MechanicResponse(BaseModel):
    mechanic_id: int
    name: str
    contact_info: str

    class Config:
        from_attributes = True

# UserRoles
class UserRoleCreate(BaseModel):
    admin_id: int
    role: str

class UserRoleResponse(BaseModel):
    user_role_id: int
    role: str
    pilot: Optional["PilotResponse"] = None
    mechanic: Optional["MechanicResponse"] = None
    customer: Optional["CustomerResponse"] = None
    admin: Optional["AdministratorResponse"] = None

    class Config:
        from_attributes = True

# Administrators
class AdministratorCreate(BaseModel):
    name: str
    contact_info: str
    role: str

class AdministratorResponse(BaseModel):
    admin_id: int
    name: str
    contact_info: str
    role: str

    class Config:
        from_attributes = True

# Licenses
class LicenseCreateRequest(BaseModel):  # 라이선스 생성 요청
    pilot_id: int
    license_number: str
    license_expiry_date: date

class LicenseResponse(BaseModel):  # 응답 데이터
    license_id: int
    pilot_id: int
    license_number: str
    license_expiry_date: date
    license_status: str
    license_document: str
    
    class Config:
        from_attributes = True
        
class LicenseUpdateRequest(BaseModel): # 라이선스 상태 수정용 테이블
    license_status: str