@echo off
rem Signal Manager Build Script for Windows
rem This script creates a standalone executable for the Signal Manager application

echo Signal Manager - Windows Build Script
echo ====================================

rem Check for Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

rem Check for required packages
echo Checking required packages...
python -m pip install -q PyQt5 pyinstaller

rem Set project directories
set PROJECT_DIR=%~dp0..\..
set RELEASE_DIR=%PROJECT_DIR%\Release\Windows

rem Create release directory if it doesn't exist
if not exist %RELEASE_DIR% mkdir %RELEASE_DIR%

rem Navigate to project directory
cd /d %PROJECT_DIR%

rem Build the executable with PyInstaller
echo Building executable with PyInstaller...
pyinstaller --noconfirm --onedir --windowed --icon=%PROJECT_DIR%\Cfg\Icons\app_icon.ico --add-data "%PROJECT_DIR%\Cfg;Cfg" --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --name=SignalManager "%PROJECT_DIR%\APP\main.py"

rem Check if build was successful
if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b %ERRORLEVEL%
)

rem Copy the dist folder to the release directory
echo Copying files to release directory...
if exist %RELEASE_DIR%\SignalManager rmdir /s /q %RELEASE_DIR%\SignalManager
xcopy /E /I /Q dist\SignalManager %RELEASE_DIR%\SignalManager

rem Cleanup
echo Cleaning up...
rmdir /s /q build dist
del SignalManager.spec

echo Build completed successfully!
echo Executable is located at: %RELEASE_DIR%\SignalManager\SignalManager.exe

exit /b 0