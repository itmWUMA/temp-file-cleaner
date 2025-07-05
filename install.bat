@echo off
REM ============================================================================
REM TempCleaner Installation Script for Windows
REM
REM This script registers TempCleaner to run automatically every hour using
REM the Windows Task Scheduler.
REM
REM It must be run with Administrator privileges to create scheduled tasks.
REM ============================================================================

set "TASK_NAME=TempCleaner"
REM %~dp0 is the directory of this batch file.
set "EXECUTABLE_PATH=%~dp0tempcleaner.exe"

echo Registering TempCleaner for scheduled execution...

REM Check if the executable exists.
REM This assumes the script is in the same directory as the packaged .exe file.
if not exist "%EXECUTABLE_PATH%" (
    echo.
    echo ERROR: Cannot find the executable at '%EXECUTABLE_PATH%'.
    echo Please make sure this script is in the same directory as tempcleaner.exe
    echo after you have packaged the application with PyInstaller.
    pause
    exit /b 1
)

echo Task Name: %TASK_NAME%
echo Executable to run: %EXECUTABLE_PATH% check-schedule

REM Create a scheduled task that runs every hour.
REM /create: Creates a new task.
REM /sc HOURLY: Specifies the schedule (every hour).
REM /tn "%TASK_NAME%": The name of the task.
REM /tr "'%EXECUTABLE_PATH%' check-schedule": The command to execute. Note the quotes.
REM /f: Force creation, overwriting any existing task with the same name.
REM /rl HIGHEST: To run with highest privileges if needed.

schtasks /create /sc HOURLY /tn "%TASK_NAME%" /tr "'%EXECUTABLE_PATH%' check-schedule" /f /rl HIGHEST

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create the scheduled task.
    echo Please make sure you are running this script as an Administrator.
    pause
) else (
    echo.
    echo SUCCESS: TempCleaner has been successfully scheduled to run every hour.
    echo You can manage this task in the Windows Task Scheduler under the name "TempCleaner".
    pause
)
