from sqlalchemy.orm import Session
from models import Administrators, AdministratorCreate, AdministratorResponse
from fastapi import HTTPException

# CREATE
def create_administrator(db: Session, administrator: AdministratorCreate) -> AdministratorResponse:
    db_administrator = Administrators(**administrator.model_dump())
    db.add(db_administrator)
    db.commit()
    db.refresh(db_administrator)
    return db_administrator

# READ ALL
def get_all_administrators(db: Session) -> list[AdministratorResponse]:
    return db.query(Administrators).all()

# UPDATE
def update_administrator(db: Session, admin_id: int, administrator: AdministratorCreate) -> AdministratorResponse:
    db_administrator = db.query(Administrators).filter(Administrators.admin_id == admin_id).first()
    if not db_administrator:
        raise HTTPException(status_code=404, detail="Administrator not found")
    for key, value in administrator.model_dump().items():
        setattr(db_administrator, key, value)
    db.commit()
    db.refresh(db_administrator)
    return db_administrator

# DELETE
def delete_administrator(db: Session, admin_id: int):
    db_administrator = db.query(Administrators).filter(Administrators.admin_id == admin_id).first()
    if not db_administrator:
        raise HTTPException(status_code=404, detail="Administrator not found")
    db.delete(db_administrator)
    db.commit()
    return {"message": f"Administrator {admin_id} deleted successfully"}
