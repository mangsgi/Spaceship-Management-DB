from sqlalchemy.orm import Session
from models import MaintenanceRecords, MaintenanceRecordCreate, MaintenanceRecordResponse
from fastapi import HTTPException

# CREATE
def create_maintenance_record(db: Session, record: MaintenanceRecordCreate) -> MaintenanceRecordResponse:
    db_record = MaintenanceRecords(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# READ ALL
def get_all_maintenance_records(db: Session) -> list[MaintenanceRecordResponse]:
    return db.query(MaintenanceRecords).all()

# UPDATE
def update_maintenance_record(db: Session, record_id: int, record: MaintenanceRecordCreate) -> MaintenanceRecordResponse:
    db_record = db.query(MaintenanceRecords).filter(MaintenanceRecords.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Maintenance Record not found")
    for key, value in record.model_dump().items():
        setattr(db_record, key, value)
    db.commit()
    db.refresh(db_record)
    return db_record

# DELETE
def delete_maintenance_record(db: Session, record_id: int):
    db_record = db.query(MaintenanceRecords).filter(MaintenanceRecords.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Maintenance Record not found")
    db.delete(db_record)
    db.commit()
    return {"message": f"Maintenance Record {record_id} deleted successfully"}
