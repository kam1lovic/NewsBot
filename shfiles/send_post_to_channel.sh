#!/bin/bash

echo "Script started at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/post_to_channel.log

source /Users/macbook/PycharmProjects/NewsBot/.venv/bin/activate

export PYTHONPATH=/Users/macbook/PycharmProjects/NewsBot

/Users/macbook/PycharmProjects/NewsBot/.venv/bin/python /Users/macbook/PycharmProjects/NewsBot/Pyrogram/py_main.py

echo "Script ended at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/post_to_channel.log


