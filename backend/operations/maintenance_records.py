from sqlalchemy.orm import Session
from models import MaintenanceRecords, MaintenanceRecordCreate, MaintenanceRecordResponse, MaintenanceTasks
from fastapi import HTTPException
from typing import Optional

# Mechanic - 유지 보수 작업 기록
def create_maintenance_record(db: Session, record: MaintenanceRecordCreate) -> MaintenanceRecordResponse:
    task = db.query(MaintenanceTasks).filter(MaintenanceTasks.task_id == record.task_id).first()
    if not task:
        raise HTTPException(status_code=400, detail=f"유지보수 작업 ID {record.task_id}를 찾을 수 없습니다.")
    
    db_record = MaintenanceRecords(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return MaintenanceRecordResponse.model_validate(db_record)

# Fin Mechanic - 유지 보수 기록 조회
def get_maintenance_record(db: Session, task_id: Optional[int] = None):
    if task_id is not None:
        maintenance_records = db.query(MaintenanceRecords).filter(MaintenanceRecords.task_id == task_id).all()
        if not maintenance_records:
            raise HTTPException(status_code=404, detail=f"Task ID {task_id}와 관련된 유지 보수 기록을 찾을 수 없습니다.")
        return [MaintenanceRecordResponse.model_validate(record) for record in maintenance_records]
    else:
        maintenance_records = db.query(MaintenanceRecords).all()
        return [MaintenanceRecordResponse.model_validate(record) for record in maintenance_records]