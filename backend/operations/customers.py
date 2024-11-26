from sqlalchemy.orm import Session
from models import Customers, CustomerCreate, CustomerResponse
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
