@echo off
cd /d "C:\Users\Strobin\Desktop\VSC\Flask\weles sql"

REM Activate virtual environment
call venv\Scripts\activate.bat


REM Open website in browser
start "" http://127.0.0.1:5000/
python run.py

pause
