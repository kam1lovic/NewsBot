import logging
import os

import openai
from dotenv import load_dotenv

from ChatGPT.prompts import main_prompts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.getenv('AI_API_KEY')


def generate_title(news: list, categories: list):
    prompt = main_prompts(categories, news)

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": prompt},
        ],
    )

    result = response['choices'][0]['message']['content'].strip()
    return result


