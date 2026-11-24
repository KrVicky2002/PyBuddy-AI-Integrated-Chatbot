import re


def generate_title(message):

    # Remove common words that don't add much meaning
    ignored_words = {
        "explain", "tell", "me", "about", "what",
        "is", "are", "the", "a", "an", "how",
        "does", "do", "with", "examples", "please"
    }

    # Remove punctuation
    message = re.sub(r"[^\w\s]", "", message)

    # Split the message into words
    words = message.split()

    # Keep meaningful words
    title_words = [
        word for word in words
        if word.lower() not in ignored_words
    ]

    # Select maximum 4 words
    title_words = title_words[:4]

    # Create the final title
    title = " ".join(title_words).title()

    return title if title else "New Chat"