import streamlit as st
import requests
import json
from typing import List, Dict, Any
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Healthcare AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #F3E5F5;
        border-left: 4px solid #9C27B0;
    }
    .context-box {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .healthcare-card {
        background-color: #E8F5E8;
        border: 1px solid #4CAF50;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #FFF3CD;
        border: 1px solid #FFC107;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_connection():
    """Check if the API server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}

def get_example_contexts():
    """Fetch example contexts from the backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}/example-contexts", timeout=5)
        if response.status_code == 200:
            return response.json().get("examples", [])
        else:
            return []
    except Exception:
        return []

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Healthcare AI Assistant</h1>', unsafe_allow_html=True)
    
    # Medical disclaimer
    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Medical Disclaimer:</strong> This AI assistant provides general health information only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for specific medical concerns.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Health Chat", "Symptom Assessment", "Medication Lookup", "Health Knowledge", "Server Status", "Configuration"]
    )
    
    # Check API connection
    api_connected = check_api_connection()
    
    if not api_connected:
        st.error("⚠️ Cannot connect to Healthcare MCP Server API. Please ensure the server is running on localhost:8000")
        st.info("To start the server, run: `python main.py`")
        return
    
    # Page routing
    if page == "Health Chat":
        health_chat_interface()
    elif page == "Symptom Assessment":
        symptom_assessment()
    elif page == "Medication Lookup":
        medication_lookup()
    elif page == "Health Knowledge":
        health_knowledge_management()
    elif page == "Server Status":
        server_status()
    elif page == "Configuration":
        configuration_page()

def health_chat_interface():
    """Healthcare chat interface for interacting with the MCP server"""
    st.header("\U0001F4AC Health Chat Interface")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "custom_context" not in st.session_state:
        st.session_state.custom_context = ""
    if "selected_examples" not in st.session_state:
        st.session_state.selected_examples = []

    # Chat parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        search_k = st.slider("Context documents", 1, 10, 5)
    with col2:
        include_context = st.checkbox("Include medical context", value=True)
    with col3:
        category = st.selectbox("Health Category", 
                               ["", "general", "symptoms", "medications", "diseases", "lifestyle", "prevention"])

    # --- Context Section ---
    st.subheader("\U0001F4DD Add Context to Your Query")
    example_contexts = get_example_contexts()
    if example_contexts:
        st.markdown("**Select example context(s):**")
        selected = st.multiselect(
            "Example Contexts", example_contexts, default=st.session_state.selected_examples, key="selected_examples")
    else:
        selected = []
        st.info("No example contexts available.")
    custom_context = st.text_area(
        "Paste your own context (optional):", value=st.session_state.custom_context, key="custom_context", height=80)

    # Combine context
    combined_context = "\n".join(selected)
    if custom_context.strip():
        combined_context = (combined_context + "\n" + custom_context.strip()).strip()

    if combined_context:
        st.markdown(f'<div class="context-box"><strong>Context to be used:</strong><br>{combined_context.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">\U0001F464 <strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">\U0001F3E5 <strong>Healthcare Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    with st.form("chat_form"):
        user_input = st.text_area("Your health question:", height=100, placeholder="Ask about symptoms, medications, health conditions, or general wellness...")
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button("Send")
        with col2:
            clear_button = st.form_submit_button("Clear Chat")

    if clear_button:
        st.session_state.messages = []
        st.rerun()

    if submit_button and user_input.strip():
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show loading spinner
        with st.spinner("Processing your health question..."):
            # Make API request
            if len(st.session_state.messages) == 1:
                # Single message - use query endpoint
                response_data = make_api_request("/query", "POST", {
                    "query": user_input,
                    "search_k": search_k,
                    "include_context": include_context,
                    "category": category if category else None,
                    "user_context": combined_context if combined_context else None
                })

                if "error" not in response_data:
                    assistant_response = response_data["response"]
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

                    # Show context if available
                    if include_context and response_data.get("context_documents"):
                        with st.expander(f"\U0001F4DA Medical Context Used ({response_data['context_used']} documents)"):
                            for i, doc in enumerate(response_data["context_documents"]):
                                st.markdown(f'<div class="context-box"><strong>Document {i+1}:</strong> {doc["text"][:200]}...</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error: {response_data['error']}")
            else:
                # Multiple messages - use conversation endpoint
                response_data = make_api_request("/conversation", "POST", {
                    "messages": st.session_state.messages,
                    "search_k": search_k,
                    "user_context": combined_context if combined_context else None
                })

                if "error" not in response_data:
                    assistant_response = response_data["response"]
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    st.error(f"Error: {response_data['error']}")

        st.rerun()

def symptom_assessment():
    """Symptom assessment interface"""
    st.header("🔍 Symptom Assessment")
    
    st.markdown("""
    <div class="healthcare-card">
        <strong>How it works:</strong> Enter your symptoms and get general health guidance. 
        This tool helps you understand potential causes and when to seek medical attention.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("symptom_form"):
        symptoms_text = st.text_area("Enter your symptoms (separate with commas):", 
                                   height=100, 
                                   placeholder="e.g., headache, fever, fatigue, nausea")
        search_k = st.slider("Medical context documents", 1, 10, 5)
        assess_button = st.form_submit_button("Assess Symptoms")
    
    if assess_button and symptoms_text.strip():
        symptoms = [s.strip() for s in symptoms_text.split(",") if s.strip()]
        
        if symptoms:
            with st.spinner("Analyzing symptoms..."):
                response_data = make_api_request("/assess-symptoms", "POST", {
                    "symptoms": symptoms,
                    "search_k": search_k
                })
                
                if "error" not in response_data:
                    st.success("✅ Symptom assessment completed")
                    
                    # Display assessment
                    st.subheader("Health Assessment")
                    st.markdown(response_data["assessment"])
                    
                    # Show context if available
                    if response_data.get("context_documents"):
                        with st.expander(f"📚 Medical Context Used ({response_data['context_used']} documents)"):
                            for i, doc in enumerate(response_data["context_documents"]):
                                st.markdown(f'<div class="context-box"><strong>Document {i+1}:</strong> {doc["text"][:200]}...</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error: {response_data['error']}")
        else:
            st.warning("Please enter at least one symptom.")

def medication_lookup():
    """Medication information lookup"""
    st.header("💊 Medication Information")
    
    st.markdown("""
    <div class="healthcare-card">
        <strong>Medication Lookup:</strong> Get general information about medications including uses, 
        side effects, and precautions. Always consult healthcare providers for specific guidance.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("medication_form"):
        medication_name = st.text_input("Medication name:", placeholder="e.g., Aspirin, Ibuprofen, Metformin")
        search_k = st.slider("Medical context documents", 1, 10, 5)
        lookup_button = st.form_submit_button("Get Information")
    
    if lookup_button and medication_name.strip():
        with st.spinner("Retrieving medication information..."):
            response_data = make_api_request("/medication-info", "POST", {
                "medication_name": medication_name,
                "search_k": search_k
            })
            
            if "error" not in response_data:
                st.success("✅ Medication information retrieved")
                
                # Display medication info
                st.subheader(f"Information about {medication_name}")
                st.markdown(response_data["information"])
                
                # Show context if available
                if response_data.get("context_documents"):
                    with st.expander(f"📚 Medical Context Used ({response_data['context_used']} documents)"):
                        for i, doc in enumerate(response_data["context_documents"]):
                            st.markdown(f'<div class="context-box"><strong>Document {i+1}:</strong> {doc["text"][:200]}...</div>', unsafe_allow_html=True)
            else:
                st.error(f"Error: {response_data['error']}")

def health_knowledge_management():
    """Healthcare knowledge base management interface"""
    st.header("📚 Health Knowledge Management")
    
    # Get current stats
    stats = make_api_request("/knowledge/stats")
    
    if "error" not in stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Documents", stats['total_documents'])
        with col2:
            st.metric("Categories", len(stats.get('categories', [])))
        with col3:
            st.metric("Collection", stats.get('collection_name', 'N/A'))
        
        # Show category breakdown
        if stats.get('category_counts'):
            st.subheader("Documents by Category")
            for category, count in stats['category_counts'].items():
                st.write(f"• {category}: {count} documents")
    else:
        st.error(f"Error getting stats: {stats['error']}")
    
    # Add documents
    st.subheader("Add Healthcare Documents")
    with st.form("add_documents_form"):
        document_text = st.text_area("Document Text:", height=150, placeholder="Enter healthcare information, medical guidelines, or health education content...")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", [
                "general", "symptoms", "medications", "diseases", 
                "lifestyle", "prevention", "nutrition", "exercise",
                "mental_health", "pediatrics", "geriatrics", "emergency"
            ])
        with col2:
            source = st.text_input("Source", placeholder="e.g., WHO, CDC, Medical Journal")
        
        metadata_text = st.text_area("Additional Metadata (JSON):", height=100, placeholder='{"author": "Dr. Smith", "year": 2023}')
        
        col1, col2 = st.columns(2)
        with col1:
            add_button = st.form_submit_button("Add Document")
        with col2:
            clear_kb_button = st.form_submit_button("Clear Knowledge Base")
    
    if add_button and document_text.strip():
        try:
            metadata = json.loads(metadata_text) if metadata_text.strip() else {}
            metadata.update({
                "category": category,
                "source": source,
                "type": "healthcare_document"
            })
            
            response = make_api_request("/knowledge/add", "POST", {
                "documents": [{"text": document_text, "metadata": metadata}]
            })
            
            if "error" not in response:
                st.success(f"✅ {response['message']}")
            else:
                st.error(f"Error: {response['error']}")
        except json.JSONDecodeError:
            st.error("Invalid JSON in metadata field")
    
    if clear_kb_button:
        response = make_api_request("/knowledge/clear", "DELETE")
        if "error" not in response:
            st.success("✅ Healthcare knowledge base cleared successfully")
        else:
            st.error(f"Error: {response['error']}")
        st.rerun()
    
    # Search knowledge base
    st.subheader("Search Healthcare Knowledge")
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        with col1:
            search_query = st.text_input("Search Query:")
        with col2:
            search_category = st.selectbox("Category Filter", ["", "general", "symptoms", "medications", "diseases", "lifestyle", "prevention"])
        
        n_results = st.slider("Number of results", 1, 20, 5)
        search_button = st.form_submit_button("Search")
    
    if search_button and search_query.strip():
        response = make_api_request("/knowledge/search", "POST", {
            "query": search_query,
            "n_results": n_results,
            "category": search_category if search_category else None
        })
        
        if "error" not in response:
            st.success(f"Found {response['count']} results")
            for i, result in enumerate(response['results']):
                with st.expander(f"Result {i+1} (Distance: {result.get('distance', 'N/A'):.3f})"):
                    st.write(f"**Text:** {result['text']}")
                    if result.get('metadata'):
                        st.write(f"**Category:** {result['metadata'].get('category', 'N/A')}")
                        st.write(f"**Source:** {result['metadata'].get('source', 'N/A')}")
        else:
            st.error(f"Error: {response['error']}")

def server_status():
    """Server status and health monitoring"""
    st.header("🔍 Server Status")
    
    # Health check
    health = make_api_request("/health")
    if "error" not in health:
        st.success("✅ Healthcare MCP Server is healthy")
        st.json(health)
    else:
        st.error("❌ Server is not responding")
        st.error(health["error"])
    
    # Configuration
    st.subheader("Current Configuration")
    config = make_api_request("/config")
    if "error" not in config:
        st.json(config)
    else:
        st.error(f"Error getting config: {config['error']}")

def configuration_page():
    """Configuration and settings page"""
    st.header("⚙️ Configuration")
    
    st.info("""
    ### Environment Variables
    Create a `.env` file in the project root with the following variables:
    
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    CHROMA_DB_PATH=./healthcare_db
    MODEL_NAME=gpt-4
    TEMPERATURE=0.3
    MAX_TOKENS=1500
    HEALTHCARE_COLLECTION=healthcare_knowledge
    ```
    """)
    
    st.subheader("Healthcare API Endpoints")
    st.code("""
    GET  /                    - Health check
    GET  /health              - Server health
    POST /query               - Process healthcare query
    POST /conversation        - Multi-turn health conversation
    POST /assess-symptoms     - Symptom assessment
    POST /medication-info     - Medication information
    POST /knowledge/add       - Add healthcare documents
    GET  /knowledge/stats     - Get knowledge base stats
    GET  /knowledge/categories - Get available categories
    DELETE /knowledge/clear   - Clear knowledge base
    POST /knowledge/search    - Search knowledge base
    GET  /config              - Get configuration
    """)
    
    st.subheader("Usage Examples")
    
    # Symptom assessment example
    st.markdown("**Symptom Assessment:**")
    st.code("""
    curl -X POST "http://localhost:8000/assess-symptoms" \\
         -H "Content-Type: application/json" \\
         -d '{"symptoms": ["headache", "fever", "fatigue"], "search_k": 5}'
    """)
    
    # Medication lookup example
    st.markdown("**Medication Information:**")
    st.code("""
    curl -X POST "http://localhost:8000/medication-info" \\
         -H "Content-Type: application/json" \\
         -d '{"medication_name": "Aspirin", "search_k": 5}'
    """)
    
    # Add healthcare document example
    st.markdown("**Add Healthcare Document:**")
    st.code("""
    curl -X POST "http://localhost:8000/knowledge/add" \\
         -H "Content-Type: application/json" \\
         -d '{"documents": [{"text": "Hypertension is high blood pressure...", "metadata": {"category": "diseases", "source": "WHO"}}]}'
    """)

if __name__ == "__main__":
    main() 