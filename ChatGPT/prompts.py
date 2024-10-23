translation_prompts_en = """
Translate the given text to English as an experienced philologist with 50 years of experience. Additionally, make corrections and edits based on meaning and context as an experienced journalist, proofreader, and editor without changing the essence of the text. The translation should not be a simple mechanical one; it needs to reflect a deep understanding of both languages and cultures.
"""
translation_prompts_ru = """
Translate the given text to Russian as an experienced philologist with 50 years of experience. Additionally, make corrections and edits based on meaning and context as an experienced journalist, proofreader, and editor without changing the essence of the text. The translation should not be a simple mechanical one; it needs to reflect a deep understanding of both languages and cultures.
"""
translation_prompts_uz = """
Translate the given text to Uzbek as an experienced philologist with 50 years of experience. Additionally, make corrections and edits based on meaning and context as an experienced journalist, proofreader, and editor without changing the essence of the text. The translation should not be a simple mechanical one; it needs to reflect a deep understanding of both languages and cultures.
"""


def main_prompts(categories, news):
    return f"""
        Create a title for each news item. Each title should contain no more than 12 words and 90 characters, and must have a predicative verb.
        Classify the following news items into one of these categories: {categories}.
        Return the response in three languages (en, uz, ru) and in JSON format as shown below:

        {{
            "category": "Category name",
            "post_link": "Post link",
            "summary": {{
                "en": "English summary",
                "uz": "Uzbek summary",
                "ru": "Russian summary"
            }}
        }}

        News: {news}.
    """
