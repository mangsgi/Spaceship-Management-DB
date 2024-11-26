from sqlalchemy.orm import Session
from models import MaintenanceTasks, MaintenanceTaskCreate, MaintenanceTaskResponse
from fastapi import HTTPException

# CREATE
def create_maintenance_task(db: Session, task: MaintenanceTaskCreate) -> MaintenanceTaskResponse:
    db_task = MaintenanceTasks(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# READ ALL
def get_all_maintenance_tasks(db: Session) -> list[MaintenanceTaskResponse]:
    return db.query(MaintenanceTasks).all()

# UPDATE
def update_maintenance_task(db: Session, task_id: int, task: MaintenanceTaskCreate) -> MaintenanceTaskResponse:
    db_task = db.query(MaintenanceTasks).filter(MaintenanceTasks.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Maintenance Task not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# DELETE
def delete_maintenance_task(db: Session, task_id: int):
    db_task = db.query(MaintenanceTasks).filter(MaintenanceTasks.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Maintenance Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": f"Maintenance Task {task_id} deleted successfully"}
