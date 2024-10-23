#!/bin/bash

LOG_FILE="/var/log/NewsBot/save_post.log"
PROJECT_DIR="/var/www/NewsBot"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_SCRIPT="$PROJECT_DIR/Pyrogram/get_posts.py"

echo "Script started at $(date)" >> $LOG_FILE

source $VENV_DIR/bin/activate

export PYTHONPATH="$PROJECT_DIR"

$VENV_DIR/bin/python $PYTHON_SCRIPT >> $LOG_FILE 2>&1

echo "Script ended at $(date)" >> $LOG_FILE
