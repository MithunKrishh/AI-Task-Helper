import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class VectorDatabase:
    def __init__(self, dim=384):
        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(dim)  
        self.vectors = []   # store embeddings
        self.texts = []     # store original texts

    def add(self, text: str):
        """Embed text and add to vector DB"""
        embedding = self.model.encode([text])
        self.index.add(embedding)
        self.vectors.append(embedding)
        self.texts.append(text)

    def search(self, query: str, k=3):
        """Search most similar items"""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.texts[idx])
        return results


if __name__ == "__main__":
    db = VectorDatabase()

    # Add some knowledge
    db.add("Zero shot prompting is asking AI to perform a task without examples")
    db.add("Few shot prompting gives the AI a few examples before asking")
    db.add("Chain of thought prompting explains reasoning step by step")

    # Query
    print("\nSearch Results:")
    results = db.search("What is zero shot prompting?")
    for r in results:
        print("-", r)
