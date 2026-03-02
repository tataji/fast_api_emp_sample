from sqlalchemy.orm import Session
from sqlalchemy import or_
import uuid

from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: str):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employee_by_email(db: Session, email: str):
    return db.query(Employee).filter(Employee.email == email).first()


def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    department: str = None,
    is_active: bool = None
):
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department.ilike(f"%{department}%"))
    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)
    return query.offset(skip).limit(limit).all()


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(
        id=str(uuid.uuid4()),
        **employee.model_dump()
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: str, updates: EmployeeUpdate):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None

    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: str):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    db.delete(db_employee)
    db.commit()
    return db_employee


def search_employees(db: Session, q: str):
    return db.query(Employee).filter(
        or_(
            Employee.name.ilike(f"%{q}%"),
            Employee.email.ilike(f"%{q}%"),
            Employee.position.ilike(f"%{q}%"),
            Employee.department.ilike(f"%{q}%"),
        )
    ).all()
