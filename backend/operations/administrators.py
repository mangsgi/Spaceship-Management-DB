from sqlalchemy.orm import Session
from models import Administrators, AdministratorCreate, AdministratorResponse
from fastapi import HTTPException
from . import user_roles

# * - 관리자 생성
def create_administrator(db: Session, admin_data: AdministratorCreate):
    if db.query(Administrators).filter(Administrators.name == admin_data.name).first():
        raise HTTPException(status_code=400, detail="이미 존재하는 관리자 이름입니다.")
    
    new_admin = Administrators(**admin_data.model_dump())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    user_roles.create_user_role(db, role="관리자", user_id=new_admin.admin_id, user_type="관리자")
    return new_admin