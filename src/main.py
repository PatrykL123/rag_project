from dotenv import load_dotenv
import os
import sys

from src.rag.generator import generate_answer

def main():
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Missing OPENAI_API_KEY in .env file")

    print("If you want to exit the chat write: exit\n\n")

    while True:

        query = input("What is your question?: ").strip()

        if not query:
            continue

        if query.lower() == "exit":
            break

        answer = generate_answer(query)
        print(f"\n\nAnswer: {answer}")
        print("-" * 40)


if __name__ == "__main__":
    main()

