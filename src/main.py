from dotenv import load_dotenv
import os

from src.rag.generator import generate_answer

def main():
    load_dotenv()

    if os.environ.get("OPENAI_API_KEY"):
        print("Openai API key is set\n\n")
    else:
        print("please provide openai API key in .env file")
        exit()

    print("If you want to exit the chat write: exit\n\n")

    while True:

        query = input("What is your question?: ")

        if not query.strip():
            continue

        if query.lower() == "exit":
            break

        answer = generate_answer(query)
        print(f"\n\nAnswer: {answer}")
        print("-" * 40)


if __name__ == "__main__":
    main()

