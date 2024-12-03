from sqlalchemy.orm import Session
from models import MaintenanceTasks, MaintenanceTaskCreate, MaintenanceTaskResponse, Spaceships, MaintenanceTaskUpdateRequest, Mechanics, MaintenanceTaskAssignments
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
    schedules = query.order_by(MaintenanceTasks.deadline).all()
    return [MaintenanceTaskResponse.model_validate(schedule) for schedule in schedules]

# Administrator - 유지 보수 일정 수정
def update_maintenance_task(db: Session, task_id: int, task_data: MaintenanceTaskUpdateRequest) -> MaintenanceTaskResponse:
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

    # 정비사 할당 업데이트 Mechanic ID List가 들어가야 함
    if task_data.assigned_mechanics is not None:
        # 기존 할당된 정비사 제거
        task.assigned_mechanics.clear()

        # 새로운 정비사 할당
        mechanics = db.query(Mechanics).filter(Mechanics.mechanic_id.in_(task_data.assigned_mechanics)).all()
        if len(mechanics) != len(task_data.assigned_mechanics):
            raise HTTPException(status_code=400, detail="할당하려는 정비사 중 일부를 찾을 수 없습니다.")
        task.assigned_mechanics.extend(mechanics)
        
    db.commit()
    db.refresh(task)
    return MaintenanceTaskResponse.model_validate(task)

# Mechanic - 본인이 할당된 유지 보수 작업 조회
def get_maintenance_tasks_by_mechanic(db: Session, mechanic_id: int) -> List[MaintenanceTaskResponse]:
    mechanic_exists = db.query(Mechanics).filter(Mechanics.mechanic_id == mechanic_id).first()
    if not mechanic_exists:
        raise HTTPException(status_code=404, detail="해당 정비사가 존재하지 않습니다.")

    tasks = (
        db.query(MaintenanceTasks)
        .join(MaintenanceTaskAssignments, MaintenanceTasks.task_id == MaintenanceTaskAssignments.task_id)
        .filter(MaintenanceTaskAssignments.mechanic_id == mechanic_id)
        .order_by(MaintenanceTasks.deadline.asc())
        .all()
    )

    if not tasks:
        return []
    return [MaintenanceTaskResponse.model_validate(task) for task in tasks]

