from sqlalchemy.orm import Session
from models import Customers, CustomerCreate, CustomerResponse, CustomerUpdateRequest
from fastapi import HTTPException
import user_roles

# * - 고객 생성
def create_customer(db: Session, customer_data: CustomerCreate):
    new_customer = Customers(**customer_data.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    user_roles.create_user_role(db, role="고객", user_id=new_customer.customer_id, user_type="고객")
    return new_customer

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