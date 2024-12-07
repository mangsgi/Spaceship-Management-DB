from sqlalchemy.orm import Session
from models import Customers, CustomerCreate, CustomerResponse, CustomerUpdateRequest
from fastapi import HTTPException
from . import user_roles
from typing import Optional

# * - 고객 생성
def create_customer(db: Session, customer_data: CustomerCreate):
    new_customer = Customers(**customer_data.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    user_roles.create_user_role(db, role="고객", user_id=new_customer.customer_id, user_type="고객")
    return CustomerResponse.model_validate(new_customer)

# FIN * - 고객 조회
def get_customers(db: Session, customer_id: Optional[int] = None):
    if customer_id is not None:
        customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="해당 고객을 찾을 수 없습니다.")
        return [CustomerResponse.model_validate(customer)]
    else:
        customers = db.query(Customers).all()
        return [CustomerResponse.model_validate(customer) for customer in customers]

# Customers - 본인의 개인정보 수정
def update_customer_information(db: Session, customer_id: int, customer_data: CustomerUpdateRequest) -> CustomerResponse:
    # 해당 고객 검색
    customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="고객을 찾을 수 없습니다.")

    # 데이터 업데이트
    if customer_data.name is not None:
        customer.name = customer_data.name
    if customer_data.contact_info is not None:
        customer.contact_info = customer_data.contact_info

    # 데이터베이스에 변경 사항 저장
    db.commit()
    db.refresh(customer)
    return CustomerResponse.model_validate(customer)

# FIN * - 고객 삭제
def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=401, detail="고객을 찾을 수 없습니다.")
    try:
        db.delete(customer)
        db.commit()
        return {"message": f"고객 '{customer_id}'가 삭제되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"고객 삭제 중 오류 발생: {str(e)}")