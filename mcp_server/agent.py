from typing import List, Dict, Any, Optional
from .vector_db import VectorDB
from .llm_handler import LLMHandler
import json

class HealthcareAgent:
    """Healthcare Agent that orchestrates the MCP Server workflow for medical applications"""
    
    def __init__(self):
        self.vector_db = VectorDB()
        self.llm_handler = LLMHandler()
        
    def process_query(self, 
                     user_input: str, 
                     search_k: int = 5,
                     include_context: bool = True,
                     category: str = None,
                     user_context: str = None) -> Dict[str, Any]:
        """Process a healthcare query through the complete pipeline"""
        
        try:
            # Step 1: Search vector database for relevant medical context
            context_documents = []
            if include_context:
                context_documents = self.vector_db.search(
                    user_input, 
                    n_results=search_k,
                    category=category
                )
            # Step 1.5: Add user_context as a pseudo-document if provided
            if user_context:
                context_documents = ([{"text": user_context, "metadata": {"source": "user_context"}}] + context_documents)
            
            # Step 2: Generate healthcare-focused response using LLM with context
            response = self.llm_handler.generate_response(
                user_message=user_input,
                context_documents=context_documents,
                include_disclaimer=True
            )
            
            # Step 3: Prepare output
            result = {
                "query": user_input,
                "response": response,
                "context_used": len(context_documents),
                "context_documents": context_documents if include_context or user_context else [],
                "category": category,
                "status": "success"
            }
            
            return result
            
        except Exception as e:
            return {
                "query": user_input,
                "response": f"Error processing query: {str(e)}",
                "context_used": 0,
                "context_documents": [],
                "status": "error",
                "error": str(e)
            }
    
    def assess_symptoms(self, symptoms: List[str], search_k: int = 5) -> Dict[str, Any]:
        """Assess symptoms and provide health guidance"""
        try:
            # Search for relevant medical information
            symptom_query = " ".join(symptoms)
            context_documents = self.vector_db.search(symptom_query, n_results=search_k)
            
            # Generate health assessment
            assessment = self.llm_handler.generate_health_assessment(
                symptoms=symptoms,
                context_documents=context_documents
            )
            
            return {
                "symptoms": symptoms,
                "assessment": assessment,
                "context_used": len(context_documents),
                "context_documents": context_documents,
                "status": "success"
            }
        except Exception as e:
            return {
                "symptoms": symptoms,
                "assessment": f"Error generating assessment: {str(e)}",
                "context_used": 0,
                "context_documents": [],
                "status": "error",
                "error": str(e)
            }
    
    def get_medication_info(self, medication_name: str, search_k: int = 5) -> Dict[str, Any]:
        """Get information about a specific medication"""
        try:
            # Search for medication-related information
            context_documents = self.vector_db.search(
                medication_name, 
                n_results=search_k,
                category="medications"
            )
            
            # Generate medication information
            info = self.llm_handler.generate_medication_info(
                medication_name=medication_name,
                context_documents=context_documents
            )
            
            return {
                "medication": medication_name,
                "information": info,
                "context_used": len(context_documents),
                "context_documents": context_documents,
                "status": "success"
            }
        except Exception as e:
            return {
                "medication": medication_name,
                "information": f"Error generating medication info: {str(e)}",
                "context_used": 0,
                "context_documents": [],
                "status": "error",
                "error": str(e)
            }
    
    def add_healthcare_knowledge(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add healthcare documents to the knowledge base"""
        try:
            self.vector_db.add_documents(documents)
            return {
                "status": "success",
                "documents_added": len(documents),
                "message": f"Successfully added {len(documents)} healthcare documents to knowledge base"
            }
        except Exception as e:
            return {
                "status": "error",
                "documents_added": 0,
                "message": f"Error adding documents: {str(e)}",
                "error": str(e)
            }
    
    def get_healthcare_stats(self) -> Dict[str, Any]:
        """Get statistics about the healthcare knowledge base"""
        try:
            all_docs = self.vector_db.get_all_documents()
            categories = self.vector_db.get_categories()
            
            # Count documents by category
            category_counts = {}
            for doc in all_docs:
                category = doc.get("metadata", {}).get("category", "uncategorized")
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return {
                "status": "success",
                "total_documents": len(all_docs),
                "categories": categories,
                "category_counts": category_counts,
                "collection_name": self.vector_db.collection_name
            }
        except Exception as e:
            return {
                "status": "error",
                "total_documents": 0,
                "categories": [],
                "category_counts": {},
                "error": str(e)
            }
    
    def search_by_category(self, query: str, category: str, n_results: int = 5) -> Dict[str, Any]:
        """Search the knowledge base within a specific category"""
        try:
            results = self.vector_db.search(query, n_results=n_results, category=category)
            return {
                "status": "success",
                "query": query,
                "category": category,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {
                "status": "error",
                "query": query,
                "category": category,
                "results": [],
                "count": 0,
                "error": str(e)
            }
    
    def get_documents_by_category(self, category: str) -> Dict[str, Any]:
        """Get all documents in a specific category"""
        try:
            documents = self.vector_db.get_documents_by_category(category)
            return {
                "status": "success",
                "category": category,
                "documents": documents,
                "count": len(documents)
            }
        except Exception as e:
            return {
                "status": "error",
                "category": category,
                "documents": [],
                "count": 0,
                "error": str(e)
            }
    
    def clear_knowledge(self) -> Dict[str, Any]:
        """Clear all documents from the knowledge base"""
        try:
            self.vector_db.clear_collection()
            return {
                "status": "success",
                "message": "Healthcare knowledge base cleared successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error clearing knowledge base: {str(e)}",
                "error": str(e)
            }
    
    def chat_conversation(self, 
                         messages: List[Dict[str, str]], 
                         search_k: int = 5,
                         user_context: str = None) -> Dict[str, Any]:
        """Handle a multi-turn healthcare conversation"""
        try:
            # Get the last user message for context search
            last_user_message = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    last_user_message = msg["content"]
                    break
            
            # Search for relevant medical context
            context_documents = []
            if last_user_message:
                context_documents = self.vector_db.search(last_user_message, n_results=search_k)
            
            # Add user_context as a pseudo-document if provided
            if user_context:
                context_documents = ([{"text": user_context, "metadata": {"source": "user_context"}}] + context_documents)
            
            # Generate response
            response = self.llm_handler.chat_conversation(
                messages=messages,
                context_documents=context_documents
            )
            
            return {
                "status": "success",
                "response": response,
                "context_used": len(context_documents),
                "context_documents": context_documents
            }
            
        except Exception as e:
            return {
                "status": "error",
                "response": f"Error in conversation: {str(e)}",
                "context_used": 0,
                "context_documents": [],
                "error": str(e)
            }

# Alias for backward compatibility
MCPAgent = HealthcareAgent 