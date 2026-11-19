# HR & Leave Management API

A REST API for managing employees, departments, leave types and leave requests. The service is built with **FastAPI** and **PostgreSQL**, uses **JWT Bearer authentication** with role-based access control, and enforces rate limits with **Redis**.

Interactive API documentation (Swagger UI) is available at `/hrms`.

---

## 1. About the App

The system covers the core workflow of an HR leave process:

1. A user registers and logs in to receive a JWT access token.
2. An HR admin creates departments and leave types.
3. Employees are linked to an existing user account, a department and (optionally) a manager.
4. Employees submit leave requests; the number of days and available balance are checked automatically.
5. HR admins or the employee's direct manager review pending requests. Approving a paid leave deducts the days from the employee's leave balance.

### Roles and permissions

| Role | Capabilities |
| --- | --- |
| `HR_ADMIN` | Full access to departments, employee profiles, leave types and all leave reviews |
| `MANAGER` | Views direct reports and reviews their leave requests |
| `EMPLOYEE` | Can create leave requests; any authenticated user can read leave types |

New accounts default to `EMPLOYEE`. Permissions are enforced with a reusable `require_roles(...)` dependency; inactive accounts are rejected when resolving the current user.

### Business rules / specification

- **Authentication**
  - Passwords are hashed with Argon2 (`pwdlib` recommended hasher); plain passwords are never stored.
  - Access tokens are JWTs signed with `HS256`, containing `sub` (user id), `email`, `role` and `exp`.
  - Access tokens expire after **15 minutes** (configurable).
  - Send tokens as `Authorization: Bearer <token>`.
- **Departments**
  - Names are unique; empty names and duplicates are rejected with `400`/`409`.
  - A department with employees assigned cannot be deleted (`409`).
- **Employees**
  - Only active users with role `EMPLOYEE` or `MANAGER` may have an employee profile.
  - Employee codes and user IDs must be unique; joining dates cannot be in the future.
  - `manager_id` in requests is the manager's **user ID**; the service resolves it to the manager's employee profile ID.
  - Initial balances: **12** annual, **6** sick and **6** casual days.
- **Leave types**
  - Codes are normalized to uppercase and must be unique; only active leave types can be requested.
  - Paid leave codes `ANNUAL`, `SICK` and `CASUAL` are mapped to the corresponding employee balance fields. Paid types without a mapping are rejected.
- **Leave requests**
  - Requested dates cannot be in the past; `start_date` must not be after `end_date`.
  - `total_days` is inclusive of both start and end dates.
  - Requests are created with status `PENDING`; balance is checked at submission time.
  - Only `PENDING` requests can be reviewed; reviewers cannot approve their own requests.
  - Managers may only review requests from their direct reports; HR admins may review any request.
  - Review status must be `APPROVED` or `REJECTED`. On approval of a paid leave, balance is re-checked and then deducted.
  - Review uses row-level locking (`SELECT ... FOR UPDATE`) so concurrent reviews cannot double-deduct a balance.
- **Rate limits**
  - `POST /auth/register`: 4/minute, `POST /auth/login`: 3/minute, `GET /auth/me`: 5/minute per client.
  - Exceeded limits return `429` with a `Retry-After` header.
- **Errors**
  - All errors share one JSON shape: `{ success, status_code, message, errors, path }`, including validation, database and unexpected errors.

---

## 2. Technologies and Methods

| Area | Technology / method |
| --- | --- |
| Language | Python 3.15+ |
| API framework | FastAPI (with `fastapi[standard]`, Pydantic v2) |
| Package management | `uv` (`pyproject.toml`, `uv.lock`) |
| Database | PostgreSQL with `psycopg` (binary) driver |
| ORM / data access | SQLAlchemy 2.x (`DeclarativeBase`, typed `Mapped` columns, `Session`) |
| Migrations | Alembic (autogenerate supported) |
| Authentication | JWT (`PyJWT`, HS256), `HTTPBearer` from FastAPI |
| Password hashing | Argon2 via `pwdlib[argon2]` |
| Caching / rate limiting | Redis via `fastapi-redis-sdk` (`redis_fastapi`), integrated in the app lifespan |
| Configuration | `pydantic-settings` with `HRMS_API_` prefixed `.env` variables, cached with `functools.lru_cache` |
| Validation | Pydantic schemas with `Field` constraints and `@model_validator` |
| Authorization | Dependency injection: `get_current_user` + `require_roles(*roles)` |
| Error handling | Centralized FastAPI exception handlers |
| Concurrency control | Pessimistic row locking (`with_for_update`) on leave review |
| Architecture | Layered design: routes → controllers → services → repositories → models |

Environment variables are loaded from `.env` (prefix `HRMS_API_`). Only non-secret values are shown below:

```dotenv
HRMS_API_DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/hrms
HRMS_API_SQL_ECHO=false
HRMS_API_JWT_SECRET_KEY=<a-long-random-secret>
HRMS_API_REDIS_URL=redis://localhost:6379/0
```

---

## 3. Folder Structure

```text
hrms-api/
├── alembic/                     # Database migrations
│   ├── env.py                   # Alembic environment; loads Base.metadata and DB URL
│   ├── script.py.mako           # Migration template
│   └── versions/                # Generated revision files
├── alembic.ini                  # Alembic configuration
├── pyproject.toml               # Project metadata, dependencies, FastAPI entrypoint
├── uv.lock                      # Locked dependency versions
├── .env                         # Local configuration (not committed)
├── src/
│   ├── main.py                  # FastAPI app, routes, Redis rate limiting, exception handlers
│   ├── api/
│   │   ├── dependencies.py      # get_current_user (Bearer token → Users)
│   │   ├── permission.py        # require_roles(...) factory
│   │   └── v1/
│   │       ├── router.py        # /api/v1 aggregator
│   │       ├── test_permission.py
│   │       └── auth/ dept/ employee/ leave_type/ leave_request/
│   │           └── router.py    # Endpoint definitions per domain
│   ├── controllers/             # Thin adapters: schemas → services → response models
│   ├── services/                # Business rules, validation, transaction boundaries
│   ├── repositories/            # SQLAlchemy queries and data access only
│   ├── models/                  # ORM table definitions and enums (_enum.py)
│   ├── schemas/                 # Pydantic request/response models
│   ├── core/
│   │   ├── config.py            # Settings loaded from .env
│   │   ├── security.py          # Hashing and JWT encode/decode
│   │   ├── exception_handlers.py
│   │   └── rate_limit.py        # Custom 429 response
│   └── database/
│       ├── base.py              # DeclarativeBase
│       └── db.py                # Engine, session factory, get_db dependency
└── README.md
```

### Layer responsibilities

- **Routers** (`src/api`) declare URLs, status codes, response models, dependencies and rate limits.
- **Controllers** convert service results into response schemas.
- **Services** own business rules and commit/rollback transactions.
- **Repositories** encapsulate queries (lookups, list filters, locked row reads).
- **Models / schemas** define the database tables and the API contract respectively.

---

## 4. Getting Started

### Prerequisites

- Python 3.15+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL and Redis running locally (or connection URLs pointing to hosted instances)

### Install and run

```bash
uv sync                                  # install dependencies
# create a .env file with the variables shown above
uv run alembic upgrade head              # apply migrations
uv run fastapi dev src/main.py           # development server with reload
```

The API then runs at `http://127.0.0.1:8000` and Swagger UI at `http://127.0.0.1:8000/hrms`.

Useful infrastructure endpoints:

| Endpoint | Description |
| --- | --- |
| `GET /` | Welcome message |
| `GET /health` | Simple health check |

### Database migrations

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
uv run alembic downgrade -1
```

---

## 5. API Endpoints

All endpoints below are prefixed with `/api/v1`. Protected endpoints require a Bearer token.

### Authentication

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | Public | Register an account (`email`, `password` ≥ 8 chars) |
| `POST` | `/auth/login` | Public | Log in; returns `access_token`, `token_type`, `email` |
| `GET` | `/auth/me` | Authenticated | Get the current user's profile |

### Departments

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/departments/create` | `HR_ADMIN` | Create a department |
| `GET` | `/departments/` | `HR_ADMIN` | List all departments |
| `PATCH` | `/departments/{department_id}` | `HR_ADMIN` | Update a department |
| `DELETE` | `/departments/{department_id}` | `HR_ADMIN` | Delete a department (blocked if employees exist) |

### Employees

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/employees/create` | `HR_ADMIN` | Create an employee profile |
| `GET` | `/employees/` | `HR_ADMIN`, `MANAGER` | List all employees (admin) or direct reports (manager) |

### Leave types

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/leave-type/create` | `HR_ADMIN` | Create a leave type |
| `PUT` | `/leave-type/{leave_type_id}` | `HR_ADMIN` | Update a leave type |
| `GET` | `/leave-type/` | Authenticated | List leave types |

### Leave requests

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/leave-request/create` | `EMPLOYEE` | Submit a leave request |
| `PATCH` | `/leave-request/{leave_request_id}/review` | `HR_ADMIN`, `MANAGER` | Approve or reject a pending request |

### Permission check examples

`GET /api/v1/permission/admin`, `GET /api/v1/permission/manager` and `GET /api/v1/permission/authendicated` are small demo endpoints that confirm role checks work.

### Error response format

```json
{
  "success": false,
  "status_code": 422,
  "message": "Validation failed",
  "errors": [{ "field": "body.password", "message": "String should have at least 8 characters" }],
  "path": "/api/v1/auth/register"
}
```

Validation errors use `422` with per-field details; business conflicts use `400`/`403`/`404`/`409`; database and unexpected errors return `500` without leaking internals.
