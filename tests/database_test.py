from database.models import (
    create_conversation,
    save_message,
    get_all_conversations,
    get_messages
)

# Create a conversation
chat_id = create_conversation("Python Learning")

# Save messages
save_message(chat_id, "user", "What is Python?")
save_message(
    chat_id,
    "assistant",
    "Python is a programming language."
)

# Retrieve conversations
chats = get_all_conversations()

for chat in chats:
    print("Chat ID:", chat["id"])
    print("Title:", chat["title"])

# Retrieve messages
messages = get_messages(chat_id)

for message in messages:
    print(message["role"], ":", message["content"])