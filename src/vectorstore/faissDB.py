from langchain_community.vectorstores import FAISS
from data.processed.dataset import documents
from src.embedding.embeddings import embeddings

db = FAISS.from_documents(documents,embeddings)

db.save_local("faiss_index")

