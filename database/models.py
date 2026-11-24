
from database.db import get_connection


def create_conversation(title="New Chat"):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO conversations (title) VALUES (?)",
        (title,)
    )

    conversation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return conversation_id


def get_all_conversations():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM conversations
        ORDER BY created_at DESC, id DESC
    """)

    conversations = cursor.fetchall()
    connection.close()

    return conversations


def save_message(conversation_id, role, content):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content)
        VALUES (?, ?, ?)
    """, (conversation_id, role, content))

    connection.commit()
    connection.close()


def get_messages(conversation_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
    """, (conversation_id,))

    messages = cursor.fetchall()
    connection.close()

    return messages


# deleting conversation
def delete_conversation(conversation_id):
    connection = get_connection()
    cursor = connection.cursor()

    # Delete messages belonging to this conversation
    cursor.execute("""
        DELETE FROM messages
        WHERE conversation_id = ?
    """, (conversation_id,))

    # Delete the conversation
    cursor.execute("""
        DELETE FROM conversations
        WHERE id = ?
    """, (conversation_id,))

    connection.commit()
    connection.close()
 
    
#updating conversation title
def update_conversation_title(conversation_id, title):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE conversations
        SET title = ?
        WHERE id = ?
    """, (title, conversation_id))

    connection.commit()
    connection.close()