from sqlalchemy.orm import Session
from models import MaintenanceTasks, MaintenanceTaskCreate, MaintenanceTaskResponse, Spaceships, MaintenanceTaskUpdateRequest
from fastapi import HTTPException
from typing import Optional, List

# Administrator - 유지 보수 일정 생성
def create_maintenance_task(db: Session, task_data: MaintenanceTaskCreate) -> MaintenanceTaskResponse:
    spaceship = db.query(Spaceships).filter(Spaceships.spaceship_id == task_data.spaceship_id).first()
    if not spaceship:
        raise HTTPException(status_code=400, detail="우주선을 찾을 수 없습니다.")
    
    db_task = MaintenanceTasks(**task_data.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return MaintenanceTaskResponse.model_validate(db_task)

# Administrator - 유지 보수 일정 조회
def get_maintenance_tasks(db: Session, spaceship_id: Optional[int] = None) -> list[MaintenanceTaskResponse]:
    query = db.query(MaintenanceTasks)
    if spaceship_id:
        query = query.filter(MaintenanceTasks.spaceship_id == spaceship_id)
    return query.order_by(MaintenanceTasks.deadline).all()

# Administrator - 유지 보수 일정 수정
def update_maintenance_task(
    db: Session, task_id: int, task_data: MaintenanceTaskUpdateRequest
) -> MaintenanceTaskResponse:
    task = db.query(MaintenanceTasks).filter(MaintenanceTasks.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=400, detail="유지 보수 작업을 찾을 수 없습니다.")
    
    if task_data.task_type is not None:
        task.task_type = task_data.task_type
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.deadline is not None:
        task.deadline = task_data.deadline
    if task_data.status is not None:
        task.status = task_data.status

    db.commit()
    db.refresh(task)
    return MaintenanceTaskResponse.model_validate(task)

# Mechanic - 유지 보수 작업 할당 조회
def get_maintenance_tasks(db: Session, task_type: Optional[str] = None, priority: Optional[int] = None, deadline: Optional[str] = None) -> List[MaintenanceTaskResponse]:
    query = db.query(MaintenanceTasks)

    if task_type:
        query = query.filter(MaintenanceTasks.task_type == task_type)
    if priority:
        query = query.filter(MaintenanceTasks.priority == priority)
    if deadline:
        query = query.filter(MaintenanceTasks.deadline <= deadline)

    return query.order_by(MaintenanceTasks.deadline).all()