from sqlalchemy.orm import Session
from models import Customers, CustomerCreate, CustomerResponse, CustomerUpdateRequest
from fastapi import HTTPException

# CREATE
def create_customer(db: Session, customer: CustomerCreate) -> CustomerResponse:
    db_customer = Customers(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# READ ALL
def get_all_customers(db: Session) -> list[CustomerResponse]:
    return db.query(Customers).all()

# UPDATE
def update_customer(db: Session, customer_id: int, customer: CustomerCreate) -> CustomerResponse:
    db_customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# DELETE
def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"message": f"Customer {customer_id} deleted successfully"}

# Customers - 본인의 개인정보 수정
def update_customer_information(
    db: Session,
    customer_id: int,
    customer_data: CustomerUpdateRequest
) -> CustomerResponse:
    
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