
from core.chatbot import get_response


conversation_history = [
    {
        "role": "user",
        "content": "What is a Python dictionary?"
    },
    {
        "role": "assistant",
        "content": "A dictionary stores information in key-value pairs."
    },
    {
        "role": "user",
        "content": "Give me a simple example."
    }
]


response = get_response(conversation_history)

print("\nPyBuddy:")
print(response)
