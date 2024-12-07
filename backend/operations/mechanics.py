from sqlalchemy.orm import Session
from models import Mechanics, MechanicCreate, MechanicResponse
from fastapi import HTTPException
from typing import Optional
from . import user_roles

# Fin 정비사 조회(id가 주어지면 해당 정비사만 조회)
def get_mechanics(db: Session, mechanic_id: Optional[int] = None) -> list[MechanicResponse]:
    if mechanic_id is not None:
        mechanic = db.query(Mechanics).filter(Mechanics.mechanic_id == mechanic_id).first()
        if not mechanic:
            raise HTTPException(status_code=404, detail="해당 정비사를 찾을 수 없습니다.")
        return [MechanicResponse.model_validate(mechanic)]  # 단일 정비사를 리스트로 반환
    else:
        mechanics = db.query(Mechanics).all()
        return [MechanicResponse.model_validate(mechanic) for mechanic in mechanics]
    
# * - 정비사 생성
def create_mechanic(db: Session, mechanic_data: MechanicCreate):
    new_mechanic = Mechanics(**mechanic_data.model_dump())
    db.add(new_mechanic)
    db.commit()
    db.refresh(new_mechanic)

    user_roles.create_user_role(db, role="정비사", user_id=new_mechanic.mechanic_id, user_type="정비사")
    return new_mechanic