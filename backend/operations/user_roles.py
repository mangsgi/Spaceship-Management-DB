from sqlalchemy.orm import Session
from models import UserRoles, UserRoleCreate, UserRoleResponse
from fastapi import HTTPException

# CREATE
def create_user_role(db: Session, user_role: UserRoleCreate) -> UserRoleResponse:
    db_user_role = UserRoles(**user_role.model_dump())
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role

# READ ALL
def get_all_user_roles(db: Session) -> list[UserRoleResponse]:
    return db.query(UserRoles).all()

# UPDATE
def update_user_role(db: Session, user_role_id: int, user_role: UserRoleCreate) -> UserRoleResponse:
    db_user_role = db.query(UserRoles).filter(UserRoles.user_role_id == user_role_id).first()
    if not db_user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    for key, value in user_role.model_dump().items():
        setattr(db_user_role, key, value)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role

# DELETE
def delete_user_role(db: Session, user_role_id: int):
    db_user_role = db.query(UserRoles).filter(UserRoles.user_role_id == user_role_id).first()
    if not db_user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    db.delete(db_user_role)
    db.commit()
    return {"message": f"User role {user_role_id} deleted successfully"}
