
import os

from dotenv import load_dotenv
from openrouter import OpenRouter

from core.prompt import SYSTEM_PROMPT


# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_ai_response(messages):

    if not API_KEY:
        raise ValueError("OpenRouter API key not found!")

    # Add system instructions before conversation messages
    complete_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + messages

    with OpenRouter(api_key=API_KEY) as client:

        response = client.chat.send(
            model="particle-ai/particle-1:free",
            messages=complete_messages,
            stream=False
        )

        return response.choices[0].message.content


# Keep the earlier function for simple one-question testing
def ask_ai(question):

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    return generate_ai_response(messages)
