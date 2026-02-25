from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import crud
import schemas
from database import engine, get_db

# Create all tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="Full CRUD API for Employee data backed by SQLite (SQLAlchemy ORM)",
    version="2.0.0"
)


# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Employee Management API 🚀",
        "docs": "/docs",
        "database": "SQLite (employees.db)"
    }


# ─── CREATE ───────────────────────────────────────────────────────────────────
@app.post("/employees", response_model=schemas.EmployeeResponse, status_code=201, tags=["Employees"])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee. Email must be unique."""
    existing = crud.get_employee_by_email(db, employee.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered.")
    return crud.create_employee(db, employee)


# ─── READ ALL ─────────────────────────────────────────────────────────────────
@app.get("/employees", response_model=List[schemas.EmployeeResponse], tags=["Employees"])
def list_employees(
    department: Optional[str] = Query(None, description="Filter by department"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=500, description="Max results"),
    db: Session = Depends(get_db)
):
    """List all employees with optional filters and pagination."""
    return crud.get_employees(db, skip=skip, limit=limit, department=department, is_active=is_active)


# ─── READ ONE ─────────────────────────────────────────────────────────────────
@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse, tags=["Employees"])
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    """Get a single employee by ID."""
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return employee


# ─── UPDATE ───────────────────────────────────────────────────────────────────
@app.patch("/employees/{employee_id}", response_model=schemas.EmployeeResponse, tags=["Employees"])
def update_employee(employee_id: str, updates: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    """Partially update an employee. Only provided fields are updated."""
    if updates.email:
        existing = crud.get_employee_by_email(db, updates.email)
        if existing and existing.id != employee_id:
            raise HTTPException(status_code=400, detail="Email is already in use by another employee.")

    updated = crud.update_employee(db, employee_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return updated


# ─── DELETE ───────────────────────────────────────────────────────────────────
@app.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    """Permanently delete an employee record."""
    deleted = crud.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return {"message": f"Employee '{deleted.name}' (ID: {employee_id}) deleted successfully."}


# ─── SEARCH ───────────────────────────────────────────────────────────────────
@app.get("/employees/search/query", response_model=List[schemas.EmployeeResponse], tags=["Employees"])
def search_employees(
    q: str = Query(..., min_length=1, description="Search term (name, email, position, department)"),
    db: Session = Depends(get_db)
):
    """Search employees by name, email, position, or department."""
    return crud.search_employees(db, q)