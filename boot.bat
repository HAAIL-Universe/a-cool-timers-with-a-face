@echo off
echo === BLUEPRINT: A cool timers with a Face — Setup ^& Run ===

REM Step 1: Check prerequisites
where python >nul 2>nul
if errorlevel 1 (echo ERROR: Python 3.12+ is required. Download from https://python.org & exit /b 1)
for /f %%v in ('python --version') do echo   %%v found

REM Step 2: Create virtual environment
if not exist ".venv" (
    echo   Creating Python virtual environment...
    python -m venv .venv
)

REM Step 3: Activate environment
call .venv\Scripts\activate.bat
echo   Virtual environment activated

REM Step 4: Install dependencies
echo   Installing dependencies...
pip install -r requirements.txt
echo   Installing dependencies in web\...
pushd web
npm install
popd

REM Step 5: Check environment configuration
if not exist ".\.env" if exist ".\.env.example" (
    copy ".\.env.example" ".\.env" >nul
    echo   Created .\.env from example
)

REM Step 6: Environment file ready
echo   Environment configured

REM Step 7: Run migrations
echo   Running database migrations...
python -m alembic upgrade head 2>nul || echo   (No migrations configured)

REM Step 8: Start the app
echo.
echo === Starting BLUEPRINT: A cool timers with a Face ===
pushd web
npm run dev
popd
