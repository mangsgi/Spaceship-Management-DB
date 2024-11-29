from sqlalchemy.orm import Session
from models import MaintenanceRecords, MaintenanceRecordCreate, MaintenanceRecordResponse
from fastapi import HTTPException

# Mechanic - 유지 보수 작업 기록하기
def create_maintenance_record(db: Session, record: MaintenanceRecordCreate) -> MaintenanceRecordResponse:
    db_record = MaintenanceRecords(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
