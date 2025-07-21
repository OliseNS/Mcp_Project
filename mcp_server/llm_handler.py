import requests
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from typing import List, Dict, Any, Optional
from .config import Config

class LLMHandler:
    """LLM Handler using OpenRouter for Healthcare Applications"""
    
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.model = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS
        self.base_url = "https://openrouter.ai/api/v1"
        
        # Healthcare-specific system prompt
        self.system_prompt = """You are a knowledgeable healthcare assistant with expertise in medical information, patient education, and health guidance. You provide accurate, evidence-based health information while always emphasizing the importance of consulting healthcare professionals for specific medical advice.

Key responsibilities:
- Provide general health information and education
- Explain medical concepts in simple terms
- Suggest lifestyle and wellness tips
- Help users understand their health better
- Always recommend consulting healthcare professionals for specific medical concerns

IMPORTANT: You are not a substitute for professional medical advice, diagnosis, or treatment. Always include appropriate medical disclaimers when discussing health topics."""
    
    def _make_openrouter_request(self, messages: List[Dict[str, str]]) -> str:
        """Make request to OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://healthcare-mcp-server.com",
            "X-Title": "Healthcare MCP Server"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    def generate_response(self, 
                         user_message: str, 
                         context_documents: List[Dict[str, Any]] = None,
                         system_prompt: str = None,
                         include_disclaimer: bool = True) -> str:
        """Generate a healthcare-focused response using OpenRouter"""
        
        # Use provided system prompt or default
        system_msg = system_prompt or self.system_prompt
        
        # Prepare context from documents
        context = ""
        if context_documents:
            context = "\n\n".join([doc["text"] for doc in context_documents])
            system_msg += f"\n\nRelevant medical information:\n{context}"
        
        # Create messages
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_message}
        ]
        
        try:
            response_text = self._make_openrouter_request(messages)
            
            # Add medical disclaimer if requested
            if include_disclaimer and Config.MEDICAL_DISCLAIMER:
                response_text += f"\n\n⚠️ **Medical Disclaimer**: {Config.MEDICAL_DISCLAIMER}"
            
            return response_text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_with_template(self, 
                             template: str, 
                             variables: Dict[str, Any],
                             context_documents: List[Dict[str, Any]] = None) -> str:
        """Generate response using a template"""
        
        # Add context if provided
        if context_documents:
            context = "\n\n".join([doc["text"] for doc in context_documents])
            variables["context"] = context
        
        # Format the template
        formatted_prompt = template.format(**variables)
        
        # Create messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": formatted_prompt}
        ]
        
        try:
            response = self._make_openrouter_request(messages)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat_conversation(self, 
                         messages: List[Dict[str, str]], 
                         context_documents: List[Dict[str, Any]] = None) -> str:
        """Handle a healthcare conversation with multiple messages"""
        
        # Prepare system message with context
        system_content = self.system_prompt
        if context_documents:
            context = "\n\n".join([doc["text"] for doc in context_documents])
            system_content += f"\n\nRelevant medical information:\n{context}"
        
        # Convert to OpenRouter format
        openrouter_messages = [{"role": "system", "content": system_content}]
        
        # Add conversation messages
        for msg in messages:
            if msg["role"] == "user":
                openrouter_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                openrouter_messages.append({"role": "assistant", "content": msg["content"]})
        
        try:
            response_text = self._make_openrouter_request(openrouter_messages)
            
            # Add medical disclaimer
            if Config.MEDICAL_DISCLAIMER:
                response_text += f"\n\n⚠️ **Medical Disclaimer**: {Config.MEDICAL_DISCLAIMER}"
            
            return response_text
        except Exception as e:
            return f"Error in conversation: {str(e)}"
    
    def generate_health_assessment(self, symptoms: List[str], context_documents: List[Dict[str, Any]] = None) -> str:
        """Generate a health assessment based on symptoms"""
        
        template = """Based on the following symptoms: {symptoms}

Please provide a general health assessment including:
1. Possible conditions these symptoms might indicate
2. General lifestyle recommendations
3. When to seek medical attention
4. Preventive measures

{context}

Remember: This is for educational purposes only and should not replace professional medical evaluation."""
        
        variables = {"symptoms": ", ".join(symptoms)}
        
        if context_documents:
            context = "\n\n".join([doc["text"] for doc in context_documents])
            variables["context"] = f"Relevant medical information:\n{context}"
        else:
            variables["context"] = ""
        
        return self.generate_with_template(template, variables)
    
    def generate_medication_info(self, medication_name: str, context_documents: List[Dict[str, Any]] = None) -> str:
        """Generate medication information"""
        
        template = """Provide information about the medication: {medication_name}

Include:
1. General purpose and uses
2. Common side effects
3. Important precautions
4. General dosage information
5. Drug interactions to be aware of

{context}

Note: Always consult with healthcare providers for specific medication guidance."""
        
        variables = {"medication_name": medication_name}
        
        if context_documents:
            context = "\n\n".join([doc["text"] for doc in context_documents])
            variables["context"] = f"Relevant medication information:\n{context}"
        else:
            variables["context"] = ""
        
        return self.generate_with_template(template, variables) 