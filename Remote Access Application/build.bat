@echo off
echo Cleaning up previous builds...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
if exist "__pycache__" rd /s /q "__pycache__"

echo Installing requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Building executable...
python -m PyInstaller --clean OwlGuard.spec

if errorlevel 1 (
    echo Build failed! Please check the error messages above.
    pause
    exit /b 1
)

echo Build complete! The executable can be found in dist/
pause 