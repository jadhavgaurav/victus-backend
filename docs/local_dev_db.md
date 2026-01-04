# Local Development with Postgres + pgvector

This project now supports PostgreSQL with the `pgvector` extension.

## 1. Start the Database

Use Docker Compose to start the Postgres service alone:

```bash
docker compose up -d db
```

This will:

- Start Postgres 16 on port 5432.
- Automatically enable the `vector` extension.
- Create a user `victus` with password `victus_dev_password` and database `victus`.

## 2. Configure Environment

Set your environment variable to point to the local Postgres instance:

```bash
export DATABASE_URL=postgresql+psycopg2://victus:victus_dev_password@localhost:5432/victus
```

## 3. Verify Connection

Run the verification script to confirm connectivity and extension availability:

```bash
python backend/scripts/db_check.py
```

Expected output:

```
Testing connection to: localhost:5432/victus (redacted)
SUCCESS: Connected to database and executed SELECT 1.
SUCCESS: 'vector' extension is installed.
```

## 4. Run Backend

You can now run the backend locally with this database:

```bash
# Ensure dependencies are installed
cd backend
poetry install

# Run migration check (optional, once migrations are added)
# poetry run alembic upgrade head

# Start app
poetry run uvicorn src.main:app --reload
```
