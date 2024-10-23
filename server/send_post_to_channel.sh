#!/bin/bash

LOG_FILE="/var/log/NewsBot/post_to_channel.log"
PROJECT_DIR="/var/www/NewsBot"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_SCRIPT="$PROJECT_DIR/Pyrogram/py_main.py"

echo "Script started at $(date)" >> $LOG_FILE

source $VENV_DIR/bin/activate

export PYTHONPATH="$PROJECT_DIR"

$VENV_DIR/bin/python $PYTHON_SCRIPT >> $LOG_FILE 2>&1

echo "Script ended at $(date)" >> $LOG_FILE
