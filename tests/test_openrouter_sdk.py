from services.ai_service import ask_ai

question = "Who won the football World Cup?"

try:
    answer = ask_ai(question)

    print("\nPyBuddy:")
    print(answer)

except Exception as e:
    print("\nError occurred:")
    print(type(e).__name__)
    print(str(e))