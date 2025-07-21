import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import os
from .config import Config

class VectorDB:
    """Vector Database handler using ChromaDB for Healthcare Knowledge"""
    
    def __init__(self, collection_name: str = None):
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection_name = collection_name or Config.HEALTHCARE_COLLECTION
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            return self.client.get_collection(name=self.collection_name)
        except:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={
                    "description": "Healthcare Knowledge Base",
                    "domain": "healthcare",
                    "version": "1.0"
                }
            )
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector database"""
        if not documents:
            return
        
        texts = [doc["text"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        ids = [doc.get("id", f"healthcare_doc_{i}") for i, doc in enumerate(documents)]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 5, category: str = None) -> List[Dict[str, Any]]:
        """Search for similar documents with optional category filter"""
        where_filter = {}
        if category:
            where_filter["category"] = category
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        documents = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                documents.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] and results["metadatas"][0] else {},
                    "id": results["ids"][0][i] if results["ids"] and results["ids"][0] else f"result_{i}",
                    "distance": results["distances"][0][i] if results["distances"] and results["distances"][0] else 0.0
                })
        
        return documents
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from the collection"""
        results = self.collection.get()
        
        documents = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"]):
                documents.append({
                    "text": doc,
                    "metadata": results["metadatas"][i] if results["metadatas"] else {},
                    "id": results["ids"][i] if results["ids"] else f"doc_{i}"
                })
        
        return documents
    
    def get_documents_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get documents by category"""
        results = self.collection.get(where={"category": category})
        
        documents = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"]):
                documents.append({
                    "text": doc,
                    "metadata": results["metadatas"][i] if results["metadatas"] else {},
                    "id": results["ids"][i] if results["ids"] else f"doc_{i}"
                })
        
        return documents
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        results = self.collection.get()
        categories = set()
        
        if results["metadatas"]:
            for metadata in results["metadatas"]:
                if metadata and "category" in metadata:
                    categories.add(metadata["category"])
        
        return list(categories)
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID"""
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"Error deleting document {doc_id}: {e}")
            return False
    
    def clear_collection(self) -> None:
        """Clear all documents from the collection"""
        self.collection.delete(where={}) 