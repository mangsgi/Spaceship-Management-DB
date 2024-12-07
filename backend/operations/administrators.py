from sqlalchemy.orm import Session
from models import Administrators, AdministratorCreate, AdministratorResponse
from fastapi import HTTPException
from . import user_roles
from typing import Optional

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

# FIN Administator - 관리자 조회 for 접속
def get_administrators(db: Session, administrator_id: Optional[int]):
    if administrator_id is not None:
        administrator = db.query(Administrators).filter(Administrators.admin_id == administrator_id).first()
        if not administrator:
            raise HTTPException(status_code=404, detail="해당 관리자를 찾을 수 없습니다.")
        return [AdministratorResponse.model_validate(administrator)]
    else:
        administrators = db.query(Administrators).all()
        return [AdministratorResponse.model_validate(administrator) for administrator in administrators]