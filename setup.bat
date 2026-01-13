@echo off
REM RoofSpec Matcher Setup Script for Windows

echo =========================================
echo RoofSpec Matcher - Setup Script
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Step 1: Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed

echo.
echo Step 4: Setting up environment file...
if exist ".env" (
    echo .env file already exists. Skipping...
) else (
    copy .env.example .env
    echo .env file created from template
    echo.
    echo WARNING: Edit the .env file and add your API key!
)

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Edit .env and add your API key (OpenAI or Anthropic)
echo 2. Activate the virtual environment: venv\Scripts\activate
echo 3. Run the application: streamlit run app.py
echo.
echo For testing PDF extraction: python test_extraction.py your_file.pdf
echo.
pause
