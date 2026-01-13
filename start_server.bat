@echo off
echo ============================================
echo PRISM Web Backend - Quick Start Script
echo ============================================
echo.

echo Step 1: Checking PostgreSQL...
echo Please ensure PostgreSQL is installed and running
echo Database: prism_db
echo User: postgres
echo Password: postgres (or your password)
echo.
echo If database is not set up, run:
echo     psql -U postgres -f database_setup.sql
echo.
pause

echo.
echo Step 2: Starting FastAPI Server...
echo.
cd backend
call venv\Scripts\activate
python main.py
