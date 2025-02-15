from sqlalchemy.orm import Session
from models import UserRoles, UserRoleCreate, UserRoleResponse
from fastapi import HTTPException
from typing import Optional

def create_user_role(db: Session, role: str, user_id: int, user_type: str) -> UserRoles:
    user_role_data = None

    if user_type == "조종사":
        user_role_data = UserRoles(pilot_id=user_id, role=role)
    elif user_type == "정비사":
        user_role_data = UserRoles(mechanic_id=user_id, role=role)
    elif user_type == "고객":
        user_role_data = UserRoles(customer_id=user_id, role=role)
    elif user_type == "관리자":
        user_role_data = UserRoles(admin_id=user_id, role=role)
    
    if not user_role_data:
        raise HTTPException(status_code=405, detail="유효하지 않은 사용자 유형입니다.")

    db.add(user_role_data)
    db.commit()
    db.refresh(user_role_data)
    return user_role_data

def get_users(db: Session, user_role_id: Optional[int] = None):
    if user_role_id is not None:
        user = db.query(UserRoles).filter(UserRoles.user_role_id == user_role_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")
        return [UserRoleResponse.model_validate(user)]
    else:
        users = db.query(UserRoles).all()
        return [UserRoleResponse.model_validate(user) for user in users]