from langchain_community.vectorstores import FAISS
from src.embedding.embeddings import embeddings

db = FAISS.load_local("faiss_index",
                      embeddings,
                      allow_dangerous_deserialization=True
                      )

retriever = db.as_retriever(search_kwargs={"k": 3})

query = "What are prerequisites for CS 225?"

results = retriever.invoke(query)

for r in results:
    print("----")
    print(r.page_content)