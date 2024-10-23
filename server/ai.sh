#!/bin/bash

LOG_FILE="/var/log/NewsBot/ai.log"
PROJECT_DIR="/var/www/NewsBot"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_SCRIPT="$PROJECT_DIR/ChatGPT/ai_main.py"

echo "Script started at $(date)" >> $LOG_FILE

source $VENV_DIR/bin/activate

export PYTHONPATH="$PROJECT_DIR"

echo "Running the main Python script..." >> $LOG_FILE
$VENV_DIR/bin/python $PYTHON_SCRIPT >> $LOG_FILE 2>&1
#
#if [ $? -eq 0 ]; then
#    echo "Main script finished successfully at $(date)" >> $LOG_FILE
#else
#    echo "Main script encountered an error at $(date)" >> $LOG_FILE
#    exit 1
#fi
#
#echo "Running the cleanup Python script..." >> $LOG_FILE
#$VENV_DIR/bin/python $PROJECT_DIR/ChatGPT/cleane_up.py >> $LOG_FILE 2>&1
#
#if [ $? -eq 0 ]; then
#    echo "Cleanup script finished successfully at $(date)" >> $LOG_FILE
#else
#    echo "Cleanup script encountered an error at $(date)" >> $LOG_FILE
#    exit 1
#fi

echo "Script ended at $(date)" >> $LOG_FILE
