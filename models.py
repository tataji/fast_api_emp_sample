from sqlalchemy import Column, String, Float, Boolean, Date
from database import Base
import uuid


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(Date, nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
