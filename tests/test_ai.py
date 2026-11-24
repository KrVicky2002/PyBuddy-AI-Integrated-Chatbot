import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


def ask_ai(question):

    response = client.chat.completions.create(
        model="particle-ai/particle-1:free",

        messages=[
            {
                "role": "system",
                "content": "You are a helpful Python programming tutor."
            },
            {
                "role": "user",
                "content": question
            }
        ],

        max_tokens=1000
    )

    # Display complete response information
    print("\n--- API RESPONSE DETAILS ---")

    print("Model:", response.model)

    print("Finish reason:", response.choices[0].finish_reason)

    print("Usage:", response.usage)

    print("Message:", response.choices[0].message)

    print("----------------------------\n")

    return response.choices[0].message.content