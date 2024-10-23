#!/bin/bash

echo "Script started at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/send_news.log

source /Users/macbook/PycharmProjects/NewsBot/.venv/bin/activate

export PYTHONPATH=/Users/macbook/PycharmProjects/NewsBot

/Users/macbook/PycharmProjects/NewsBot/.venv/bin/python /Users/macbook/PycharmProjects/NewsBot/send_news_to_user.py

echo "Script ended at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/send_news.log


