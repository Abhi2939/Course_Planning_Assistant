from langchain_community.vectorstores import FAISS
from src.embedding.embeddings import embeddings


def get_retriever():
    db = FAISS.load_local("faiss_index",
                          embeddings,
                          allow_dangerous_deserialization=True
                          )
    return db

def search(query):
    db = get_retriever()

    retriever = db.as_retriever(search_kwargs={"k": 5})

    results = retriever.invoke(query)

    print(f"\n🔍 Query: {query}\n")

    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Type: {r.metadata.get('type')}")
        print(r.page_content[:500]) 

if __name__ == "__main__":
    search("What are prerequisites for CS 225?")
    