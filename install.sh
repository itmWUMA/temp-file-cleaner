#!/bin/bash
# ============================================================================
# TempCleaner Installation Script for Linux and macOS
#
# This script registers TempCleaner to run automatically every hour using
# cron.
# ============================================================================

TASK_NAME="TempCleaner"
FREQUENCY_IN_MINUTES=15

# Get the absolute path to the directory containing this script.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
EXECUTABLE_PATH="$SCRIPT_DIR/tempcleaner" # The name of the PyInstaller executable on Linux/macOS

echo "Registering TempCleaner for scheduled execution..."

# Check if the executable exists.
# This assumes the script is in the same directory as the packaged executable.
if [ ! -f "$EXECUTABLE_PATH" ]; then
    echo ""
    echo "ERROR: Cannot find the executable at '$EXECUTABLE_PATH'."
    echo "Please make sure this script is in the same directory as the 'tempcleaner' executable"
    echo "after you have packaged the application with PyInstaller."
    exit 1
fi

echo "Task Name: $TASK_NAME"
echo "Executable to run: $EXECUTABLE_PATH check-schedule"
echo "Frequency set to every $FREQUENCY_IN_MINUTES minutes."

# --- 1. Create Scheduled Task (for 'schedule' triggers) ---
echo "Creating scheduled task..."
SCHEDULE_JOB="*/$FREQUENCY_IN_MINUTES * * * * '$EXECUTABLE_PATH' check-schedule # $TASK_NAME - Scheduled"

# --- 2. Create Startup Task (for 'on_startup' triggers) ---
echo "Creating startup task..."
STARTUP_JOB="@reboot '$EXECUTABLE_PATH' on-startup # $TASK_NAME - On Startup"

# --- Update Crontab ---
# Remove all old TempCleaner jobs first.
CLEANED_CRONTAB=$(crontab -l 2>/dev/null | grep -Fv "# $TASK_NAME")

# Add the new jobs.
(echo "$CLEANED_CRONTAB" ; echo "$SCHEDULE_JOB" ; echo "$STARTUP_JOB") | crontab -

if [ $? -eq 0 ]; then
    echo "SUCCESS: Scheduled and startup tasks have been configured in your crontab."
    echo "You can manage them by running 'crontab -e'."
else
    echo "ERROR: Failed to modify the crontab."
    exit 1
fi

# --- 3. Instructions for Shutdown Task (for 'on_shutdown' triggers) ---
echo ""
echo "--- Manual instructions for Shutdown task ---"
echo "To run a script on shutdown, the method depends on your system:"
echo " - For systems using 'systemd', you can create a service in /etc/systemd/system/."
echo " - For older systems, you might place a script in /etc/rc.d/rc.0/."
echo "Automating this is complex and system-specific, so manual setup is recommended if needed."

echo ""
echo "=========================================="
echo "Installation complete."
echo "=========================================="
