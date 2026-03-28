from langchain_community.vectorstores import FAISS
from data.processed.dataset import documents
from src.embedding.embeddings import embeddings
import os

def build_faiss():

    print(f"📄 Total documents: {len(documents)}")
    print("🔄 Creating FAISS index...")

    db = FAISS.from_documents(documents,embeddings)

    save_path = os.path.join(os.getcwd(), "faiss_index")
    db.save_local(save_path)

    print("✅ FAISS index saved at:", save_path)

if __name__ == "__main__":
    build_faiss()

