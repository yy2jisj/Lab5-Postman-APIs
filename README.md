# Lab 5 - Postman and APIs

Flask REST API backed by SQLite for CRUD user management.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Base URL: `http://localhost:5000`

| Method | Endpoint |
| --- | --- |
| GET | `/api/users` |
| GET | `/api/users/<user_id>` |
| POST | `/api/users/add` |
| PUT | `/api/users/update` |
| DELETE | `/api/users/delete/<user_id>` |

Postman collection: `postman/Flask-user-app.postman_collection.json`

Postman environment: `postman/Flask-user-app.postman_environment.json`

Run `python scripts/verify_api.py` while the server is running to verify every CRUD endpoint with real HTTP requests.

Verification screenshots: `screenshots/`

## Manual corrections

Python already includes `sqlite3`, so the manual's `pip install db-sqlite3` command is not needed. The working implementation also corrects `conn().rollback()` to `conn.rollback()`, uses valid multiline SQL, creates the table only when needed, and closes every database connection.
