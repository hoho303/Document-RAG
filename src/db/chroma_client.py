import chromadb
import numpy as np
import os
import dotenv

dotenv.load_dotenv()

class ChromaRetriever:
    def __init__(self, client, collection_name: str):
        self.collection_name = collection_name
        self.client = client
        if self.client.get_collection(collection_name):
            self.client.delete_collection(collection_name)

    def create_collection(self):
        self.collection = self.client.get_or_create_collection(self.collection_name)
        
    def add_image_embeddings(self, batch_data: list):
        ids = [data["id"] for data in batch_data]
        embeddings = [data["embedding"] for data in batch_data]
        image_names = [data["image_name"] for data in batch_data]

        return self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=[{"image_name": image_name} for image_name in image_names]
            )

    def query_image_embeddings(self, collection_name: str, query_embedding: np.ndarray, n_results: int = 5):
        return self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
        )

    def delete_collection(self):
        return self.client.delete_collection(self.collection_name)
