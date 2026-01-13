# Quick Start Guide (Without PostgreSQL)

## Option 1: Install PostgreSQL (Recommended)

### Download and Install:

1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Set password for postgres user (remember this!)
4. Default port: 5432

### Setup Database:

```bash
# Open Command Prompt or PowerShell as Administrator
cd "C:\Program Files\PostgreSQL\<version>\bin"

# Connect to PostgreSQL
psql -U postgres

# Run the setup script
\i C:/Users/user/Desktop/test2/backend/database_setup.sql
```

## Option 2: Use SQLite (Quick Testing)

For quick testing without PostgreSQL, I'll create a mock version.

## Option 3: Use Docker PostgreSQL

```bash
docker run --name prism-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=prism_db -p 5432:5432 -d postgres:15
```

Then run the database_setup.sql file.
