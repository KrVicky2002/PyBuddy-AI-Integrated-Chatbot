
from services.ai_service import generate_ai_response


def get_response(conversation_history):

    if not conversation_history:
        raise ValueError("Conversation history cannot be empty.")

    response = generate_ai_response(conversation_history)

    return response
