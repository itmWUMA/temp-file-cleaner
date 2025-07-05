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
set "FREQUENCY_IN_MINUTES=15"

REM %~dp0 is the directory of this batch file.
set "EXECUTABLE_PATH=%~dp0tempcleaner.exe"

echo Registering TempCleaner for scheduled execution...
echo Frequency set to every %FREQUENCY_IN_MINUTES% minutes.

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

REM --- 1. Create Scheduled Task (for 'schedule' triggers) ---
echo Creating scheduled task...
schtasks /create /sc MINUTE /mo %FREQUENCY_IN_MINUTES% /tn "%TASK_NAME% - Scheduled" /tr "'%EXECUTABLE_PATH%' check-schedule" /f /rl HIGHEST

if %errorlevel% neq 0 (
    echo ERROR: Failed to create the scheduled task.
) else (
    echo SUCCESS: Scheduled task created.
)

REM --- 2. Create Startup Task (for 'on_startup' triggers) ---
echo.
echo Creating startup task...
schtasks /create /sc ONLOGON /tn "%TASK_NAME% - On Startup" /tr "'%EXECUTABLE_PATH%' on-startup" /f /rl HIGHEST

if %errorlevel% neq 0 (
    echo ERROR: Failed to create the startup task.
) else (
    echo SUCCESS: Startup task created.
)

REM --- 3. Instructions for Shutdown Task (for 'on_shutdown' triggers) ---
echo.
echo --- Manual instructions for Shutdown task ---
echo To run a task on shutdown, you need to use the Group Policy Editor:
echo  1. Press Win+R, type 'gpedit.msc' and press Enter.
echo  2. Navigate to: Computer Configuration ^> Windows Settings ^> Scripts (Startup/Shutdown).
echo  3. Double-click "Shutdown" in the right pane.
echo  4. Click "Add...", and in "Script Name", enter: '%EXECUTABLE_PATH%'
echo  5. In "Script Parameters", enter: 'on-shutdown'
echo This is the most reliable way to configure shutdown scripts in Windows.

echo.
echo ===========================================
echo Installation complete.
echo Please review any errors above.
echo ===========================================
pause
