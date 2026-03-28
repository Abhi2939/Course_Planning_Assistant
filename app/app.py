from src.pipeline.rag_pipeline import ask

def main():
    print("🎓 Course Planning Assistant (RAG)")
    print("Type 'exit' to quit\n")

    print("Example questions:")
    print("- What are prerequisites for CS 225?")
    print("- Can I take CS 374 after CS 225?")
    print("- What are grading policies?\n")

    while True:
        query = input("Ask your question: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break

        if not query.strip():
            print("⚠️ Please enter a valid question.\n")
            continue

        try:
            print("\n⏳ Thinking...\n")

            response = ask(query)

            print("📌 Response:\n")
            print(response)
            print("\n" + "=" * 60 + "\n")

        except Exception as e:
            print("❌ Something went wrong. Please try again.")
            print("Details:", str(e))


if __name__ == "__main__":
    main()