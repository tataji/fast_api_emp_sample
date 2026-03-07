# Employee Management API — FastAPI + SQLAlchemy CRUD

## Project Structure

```
employee_api/
├── main.py          # FastAPI app & route handlers
├── database.py      # DB engine, session, Base
├── models.py        # SQLAlchemy ORM model
├── schemas.py       # Pydantic request/response schemas
├── crud.py          # DB query functions
├── requirements.txt
└── employees.db     # Auto-created SQLite database
```

## Setup & Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

| Method | Endpoint                        | Description               |
|--------|---------------------------------|---------------------------|
| GET    | /                               | Health check              |
| POST   | /employees                      | Create employee           |
| GET    | /employees                      | List employees (filtered) |
| GET    | /employees/{id}                 | Get employee by ID        |
| PATCH  | /employees/{id}                 | Partially update employee |
| DELETE | /employees/{id}                 | Delete employee           |
| GET    | /employees/search/query?q=...   | Full-text search          |

### Query Parameters — GET /employees
| Param        | Type    | Description                    |
|--------------|---------|--------------------------------|
| `department` | string  | Filter by department (partial) |
| `is_active`  | boolean | Filter by active status        |
| `skip`       | int     | Pagination offset (default 0)  |
| `limit`      | int     | Max results (default 100)      |

---

## Example Payload — Create Employee

```json
{
  "name": "Jane Smith",
  "email": "jane.smith@company.com",
  "department": "Engineering",
  "position": "Senior Developer",
  "salary": 95000.0,
  "hire_date": "2024-06-01",
  "phone": "+1-555-0199",
  "is_active": true
}
```

---

## Switch to PostgreSQL

In `database.py`, replace the `DATABASE_URL`:

```python
DATABASE_URL = "postgresql://user:password@localhost:5432/employee_db"
```

And install the driver:
```bash
pip install psycopg2-binary
```

---

## Notes
- The SQLite database file (`employees.db`) is created automatically on first run.
- Employee IDs are auto-generated UUIDs.
- Email uniqueness is enforced at the DB level.
- All tables are created automatically via `Base.metadata.create_all()`.
