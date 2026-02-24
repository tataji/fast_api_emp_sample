from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import date
import uuid

app = FastAPI(
    title="Employee Management API",
    description="CRUD operations for Employee data",
    version="1.0.0"
)

# ─── In-memory database ───────────────────────────────────────────────────────
employees_db: dict = {}


# ─── Schemas ──────────────────────────────────────────────────────────────────
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="John Doe")
    email: str = Field(..., example="john.doe@example.com")
    department: str = Field(..., example="Engineering")
    position: str = Field(..., example="Software Engineer")
    salary: float = Field(..., gt=0, example=75000.0)
    hire_date: date = Field(..., example="2024-01-15")
    phone: Optional[str] = Field(None, example="+1-555-0100")
    is_active: bool = Field(default=True)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = Field(None, gt=0)
    hire_date: Optional[date] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class EmployeeResponse(EmployeeBase):
    id: str

    class Config:
        from_attributes = True


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
def root():
    return {"message": "Employee Management API is running 🚀", "docs": "/docs"}


# CREATE
@app.post("/employees", response_model=EmployeeResponse, status_code=201, tags=["Employees"])
def create_employee(employee: EmployeeCreate):
    """Create a new employee record."""
    # Check duplicate email
    for emp in employees_db.values():
        if emp["email"] == employee.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    emp_id = str(uuid.uuid4())
    emp_data = {"id": emp_id, **employee.model_dump()}
    employees_db[emp_id] = emp_data
    return emp_data


# READ ALL
@app.get("/employees", response_model=List[EmployeeResponse], tags=["Employees"])
def get_all_employees(
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    """Retrieve all employees with optional filters."""
    employees = list(employees_db.values())

    if department:
        employees = [e for e in employees if e["department"].lower() == department.lower()]
    if is_active is not None:
        employees = [e for e in employees if e["is_active"] == is_active]

    return employees[skip: skip + limit]


# READ ONE
@app.get("/employees/{employee_id}", response_model=EmployeeResponse, tags=["Employees"])
def get_employee(employee_id: str):
    """Retrieve a single employee by ID."""
    emp = employees_db.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


# UPDATE (partial)
@app.patch("/employees/{employee_id}", response_model=EmployeeResponse, tags=["Employees"])
def update_employee(employee_id: str, updates: EmployeeUpdate):
    """Partially update an employee record."""
    emp = employees_db.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check email uniqueness if changing email
    if updates.email and updates.email != emp["email"]:
        for other in employees_db.values():
            if other["email"] == updates.email and other["id"] != employee_id:
                raise HTTPException(status_code=400, detail="Email already in use")

    update_data = updates.model_dump(exclude_unset=True)
    emp.update(update_data)
    employees_db[employee_id] = emp
    return emp


# DELETE
@app.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: str):
    """Delete an employee record."""
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees_db[employee_id]
    return {"message": f"Employee {employee_id} deleted successfully"}


# SEARCH
@app.get("/employees/search/query", response_model=List[EmployeeResponse], tags=["Employees"])
def search_employees(q: str):
    """Search employees by name, email, or position."""
    q_lower = q.lower()
    results = [
        emp for emp in employees_db.values()
        if q_lower in emp["name"].lower()
        or q_lower in emp["email"].lower()
        or q_lower in emp["position"].lower()
    ]
    return results
