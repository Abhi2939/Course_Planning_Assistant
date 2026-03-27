from src.pipeline.rag_pipeline import ask

def main():
    print("Course Planning Assistant (RAG)")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Ask your question: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye")
            break

        try:
            response = ask(query)
            print("\nResponse:\n")
            print(response)
            print("\n" + "="*60 + "\n")

        except Exception as e:
            print("Error:", str(e))


if __name__ == "__main__":
    main()