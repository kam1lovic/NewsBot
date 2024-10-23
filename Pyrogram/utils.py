import random
import re


def link_random_word(content, post_link):
    content = re.sub(r'http[s]?://\S+', '', content)
    words = [word for word in content.split() if len(word) > 1 and word.isalnum()]

    if words:
        random_word = random.choice(words)
        linked_word = f"[{random_word}]({post_link})"
        content = content.replace(random_word, linked_word, 1)
    return content.strip()
