import asyncio
import os
import openai
from dotenv import load_dotenv
import logging

from ChatGPT.prompts import main_prompts, translation_prompts_en, translation_prompts_ru, translation_prompts_uz

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


async def translate_text(text: str, target_language: str) -> str:
    try:
        if target_language == "en":
            translation_prompt = translation_prompts_en
        elif target_language == "ru":
            translation_prompt = translation_prompts_ru
        elif target_language == "uz":
            translation_prompt = translation_prompts_uz
        else:
            return text

        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": translation_prompt,
                },
                {"role": "user", "content": text},
            ],
        )
        translated_text = response['choices'][0]['message']['content'].strip()
        return translated_text
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        return text
