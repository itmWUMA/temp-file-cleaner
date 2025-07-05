#!/bin/bash
# ============================================================================
# TempCleaner Installation Script for Linux and macOS
#
# This script registers TempCleaner to run automatically every hour using
# cron.
# ============================================================================

TASK_NAME="TempCleaner"
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

# Cron job that runs at the beginning of every hour.
# The comment '# TempCleaner Job' is added to make it easy to identify and remove.
CRON_JOB="0 * * * * '$EXECUTABLE_PATH' check-schedule # $TASK_NAME"

# Check if the cron job already exists to avoid duplicates.
# We use a unique comment to identify our job.
(crontab -l 2>/dev/null | grep -Fq "# $TASK_NAME")
if [ $? -eq 0 ]; then
    echo "A TempCleaner job already exists in your crontab. It will be replaced."
    # Remove the old job(s).
    (crontab -l 2>/dev/null | grep -Fv "# $TASK_NAME" ; echo "$CRON_JOB") | crontab -
else
    # Add the new cron job.
    (crontab -l 2>/dev/null ; echo "$CRON_JOB") | crontab -
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "SUCCESS: TempCleaner has been successfully scheduled to run every hour."
    echo "A new entry has been added to your crontab. You can edit it by running 'crontab -e'."
else
    echo ""
    echo "ERROR: Failed to modify the crontab."
    echo "Please check your permissions or try adding the job manually by running 'crontab -e'."
fi
