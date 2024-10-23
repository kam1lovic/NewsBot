#!/bin/bash

echo "Script started at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/ai.log

source /Users/macbook/PycharmProjects/NewsBot/.venv/bin/activate

export PYTHONPATH="/Users/macbook/PycharmProjects/NewsBot/"

echo "Running the main Python script..." >> /Users/macbook/PycharmProjects/NewsBot/logs/ai.log

/Users/macbook/PycharmProjects/NewsBot/.venv/bin/python /Users/macbook/PycharmProjects/NewsBot/ChatGPT/ai_main.py >> /Users/macbook/PycharmProjects/NewsBot/logs/ai.log 2>&1
#
#if [ $? -eq 0 ]; then
#    echo "Main script finished successfully at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/outputai.log
#else
#    echo "Main script encountered an error at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/outputai.log
#    exit 1
#fi
#
#echo "Running the cleanup Python script..." >> /Users/macbook/PycharmProjects/NewsBot/logs/outputai.log
#/Users/macbook/PycharmProjects/NewsBot/.venv/bin/python /Users/macbook/PycharmProjects/NewsBot/ChatGPT/cleane_up.py >> /Users/macbook/PycharmProjects/NewsBot/logs/cleanup.log 2>&1
#
#if [ $? -eq 0 ]; then
#    echo "Cleanup script finished successfully at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/outputai.log
#else
#    echo "Cleanup script encountered an error at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/outputai.log
#    exit 1
#fi
echo "Script ended at $(date)" >> /Users/macbook/PycharmProjects/NewsBot/logs/ai.log
