#!/bin/bash

LOG_FILE="/var/log/NewsBot/send_news.log"
PROJECT_DIR="/var/www/NewsBot"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_SCRIPT1="$PROJECT_DIR/send_news_to_user.py"
PYTHON_SCRIPT2="$PROJECT_DIR/send_news_to_channel.py"

echo "Script started at $(date)" >> $LOG_FILE

source $VENV_DIR/bin/activate

export PYTHONPATH="$PROJECT_DIR"

$VENV_DIR/bin/python $PYTHON_SCRIPT1 >> $LOG_FILE 2>&1
$VENV_DIR/bin/python $PYTHON_SCRIPT2 >> $LOG_FILE 2>&1

echo "Script ended at $(date)" >> $LOG_FILE
