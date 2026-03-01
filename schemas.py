from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Jane Smith")
    email: str = Field(..., example="jane.smith@company.com")
    department: str = Field(..., example="Engineering")
    position: str = Field(..., example="Software Engineer")
    salary: float = Field(..., gt=0, example=75000.0)
    hire_date: date = Field(..., example="2024-01-15")
    phone: Optional[str] = Field(None, example="+1-555-0100")
    is_active: bool = Field(default=True)


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = Field(None, gt=0)
    hire_date: Optional[date] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class EmployeeResponse(BaseModel):
    id: str
    name: str
    email: str
    department: str
    position: str
    salary: float
    hire_date: date
    phone: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode=True for Pydantic v1)
