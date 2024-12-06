from sqlalchemy.orm import Session
from models import MaintenanceRecords, MaintenanceRecordCreate, MaintenanceRecordResponse, MaintenanceTasks
from fastapi import HTTPException

# Mechanic - 유지 보수 작업 기록하기
def create_maintenance_record(db: Session, record: MaintenanceRecordCreate) -> MaintenanceRecordResponse:
    task = db.query(MaintenanceTasks).filter(MaintenanceTasks.task_id == record.task_id).first()
    if not task:
        raise HTTPException(status_code=400, detail=f"유지보수 작업 ID {record.task_id}를 찾을 수 없습니다.")
    
    db_record = MaintenanceRecords(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return MaintenanceRecordResponse.model_validate(db_record)
