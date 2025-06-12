# Cost Sync API

This project is a Flask-based REST API using PostgreSQL and the repository pattern. It provides endpoints for user registration, login, and logout.

## Features
- User registration
- User login
- User logout
- Repository pattern for data access

## Requirements
- Python 3.8+
- PostgreSQL
- pip

## Setup
1. Create a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your PostgreSQL database and update the database URI in the configuration.
4. Run the application:
   ```sh
   flask run
   ```

## Docker Setup

1. Build and start the services:
   ```sh
   docker-compose up --build
   ```
2. The Flask API will be available at `http://localhost:5000` and PostgreSQL at `localhost:5432`.
3. Update your application to use the `DATABASE_URL` environment variable for the database connection string.

## API Endpoints
- `POST /register` - Register a new user
- `POST /login` - Login and receive a token
- `POST /logout` - Logout the current user
- `GET /ping` - Health check, returns 'pong' if the server is live

## Project Structure
- `app/` - Main application code
- `app/repositories/` - Repository pattern implementations
- `app/models/` - Database models
- `app/routes/` - API route handlers

## Database Management

### Accessing the Database
- You can connect to the PostgreSQL database using any client (psql, DBeaver, TablePlus, etc.) with:
  - **Host:** localhost
  - **Port:** 5432
  - **Database:** cost_sync_db
  - **Username:** user
  - **Password:** password
- Example using psql:
  ```sh
  psql -h localhost -U user -d cost_sync_db
  ```

### Running Migrations (Docker)
1. Make sure your services are running:
   ```sh
   docker-compose up --build
   ```
2. In a new terminal, apply migrations:
   ```sh
   docker-compose exec web flask db upgrade
   ```

### Troubleshooting
- If you only see the `alembic_version` table after migration, ensure your models are imported in `app/__init__.py`:
  ```python
  from app.models import user
  ```
- Then re-run:
  ```sh
  docker-compose exec web flask db migrate -m "Add user table"
  docker-compose exec web flask db upgrade
  ```

---
