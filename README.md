# 🏥 Healthcare MCP Server - AI-Powered Health Assistant

A healthcare-focused MCP (Model Context Protocol) Server implementation with Vector Database and LLM integration via OpenRouter, featuring a modern Streamlit interface for medical information, symptom assessment, and health guidance.

## 🏗️ Architecture

```
Input Handler → Vector DB → Agent → LLM → Output
     ↓              ↓         ↓      ↓      ↓
  FastAPI      ChromaDB   HealthcareAgent  OpenRouter  Health Response
```

### Components

- **Input Handler**: FastAPI server with healthcare-specific endpoints
- **Vector DB**: ChromaDB for medical document storage and semantic search
- **Agent**: HealthcareAgent orchestrates medical workflows
- **LLM**: OpenRouter integration for access to multiple AI models
- **Output**: Healthcare responses with medical disclaimers

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenRouter API Key
- Docker (optional)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Mcp_Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
CHROMA_DB_PATH=./healthcare_db
MODEL_NAME=openai/gpt-4
TEMPERATURE=0.3
MAX_TOKENS=1500
HEALTHCARE_COLLECTION=healthcare_knowledge
MEDICAL_DISCLAIMER=This AI assistant provides general health information only and should not replace professional medical advice, diagnosis, or treatment.
```

### 4. Start the Server

#### Option A: Direct Python
```bash
python main.py
```

#### Option B: Module
```bash
python -m mcp_server.api
```

### 5. Launch Healthcare Interface

```bash
streamlit run streamlit_app.py
```

## 🚀 Deployment on Railway

1. **Set environment variables**: Ensure you have a `.env` file with your OpenRouter API key and any other required settings (see `mcp_server/config.py`).

2. **Deploy**: Push your repository to Railway.

3. **Service settings**:
   - Set the start command to `python main.py`.
   - Set the service port to `8000`.

4. **Access**: Once deployed, your MCP server will be available at `https://<your-railway-app>.railway.app/` and will respond to health checks at `/health`.

**Note:** Streamlit is no longer included or required for this deployment.

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Using Docker

```bash
# Build image
docker build -t healthcare-mcp-server .

# Run container
docker run -p 8000:8000 -p 8501:8501 --env-file .env healthcare-mcp-server
```

## 📡 Healthcare API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Server health status |
| `POST` | `/query` | Process healthcare query |
| `POST` | `/conversation` | Multi-turn health conversation |
| `GET` | `/config` | Get configuration |

### Healthcare-Specific Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/assess-symptoms` | Symptom assessment and guidance |
| `POST` | `/medication-info` | Medication information lookup |
| `POST` | `/knowledge/add` | Add healthcare documents |
| `GET` | `/knowledge/stats` | Get knowledge base statistics |
| `GET` | `/knowledge/categories` | Get available health categories |
| `DELETE` | `/knowledge/clear` | Clear knowledge base |
| `POST` | `/knowledge/search` | Search healthcare knowledge |

## 💬 Healthcare Usage Examples

### Symptom Assessment

```bash
curl -X POST "http://localhost:8000/assess-symptoms" \
     -H "Content-Type: application/json" \
     -d '{
       "symptoms": ["headache", "fever", "fatigue"],
       "search_k": 5
     }'
```

### Medication Information

```bash
curl -X POST "http://localhost:8000/medication-info" \
     -H "Content-Type: application/json" \
     -d '{
       "medication_name": "Aspirin",
       "search_k": 5
     }'
```

### Health Query

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the symptoms of diabetes?",
       "search_k": 5,
       "category": "diseases"
     }'
```

### Add Healthcare Document

```bash
curl -X POST "http://localhost:8000/knowledge/add" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": [
         {
           "text": "Hypertension, or high blood pressure, is a common condition that affects the body's arteries...",
           "metadata": {
             "category": "diseases",
             "source": "WHO",
             "author": "Dr. Smith"
           }
         }
       ]
     }'
```

## 🎨 Healthcare Streamlit Interface

The Streamlit interface provides:

- **Health Chat**: Interactive conversation with healthcare AI assistant
- **Symptom Assessment**: Analyze symptoms and get health guidance
- **Medication Lookup**: Get information about medications
- **Health Knowledge**: Manage medical documents and knowledge base
- **Server Status**: Monitor server health and configuration
- **Configuration**: View and manage healthcare settings

Access at: `http://localhost:8501`

## 🔧 Healthcare Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | Required | Your OpenRouter API key |
| `MODEL_NAME` | `openai/gpt-4` | OpenRouter model to use |
| `TEMPERATURE` | `0.3` | Model temperature (lower for medical accuracy) |
| `MAX_TOKENS` | `1500` | Maximum tokens per response |
| `CHROMA_DB_PATH` | `./healthcare_db` | Vector database path |
| `HEALTHCARE_COLLECTION` | `healthcare_knowledge` | Medical knowledge collection |
| `MEDICAL_DISCLAIMER` | Custom | Medical disclaimer text |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |

### Available OpenRouter Models

You can use any model available through OpenRouter. Some popular options:

- `openai/gpt-4` - OpenAI's GPT-4
- `openai/gpt-3.5-turbo` - OpenAI's GPT-3.5 Turbo
- `anthropic/claude-3-opus` - Anthropic's Claude 3 Opus
- `anthropic/claude-3-sonnet` - Anthropic's Claude 3 Sonnet
- `google/gemini-pro` - Google's Gemini Pro
- `meta-llama/llama-2-70b-chat` - Meta's Llama 2 70B

## 📁 Project Structure

```
Mcp_Project/
├── mcp_server/           # Main package
│   ├── __init__.py
│   ├── config.py         # Healthcare configuration
│   ├── vector_db.py      # ChromaDB for medical documents
│   ├── llm_handler.py    # OpenRouter integration
│   ├── agent.py          # Healthcare agent logic
│   └── api.py           # FastAPI server with health endpoints
├── streamlit_app.py      # Healthcare Streamlit interface
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose
└── README.md           # This file
```

## 🏥 Healthcare Features

### Medical Knowledge Management
- **Categorized Storage**: Organize medical information by categories (symptoms, medications, diseases, etc.)
- **Semantic Search**: Find relevant medical information using natural language
- **Source Tracking**: Track the source and credibility of medical information

### Symptom Assessment
- **Multi-symptom Analysis**: Assess multiple symptoms together
- **Health Guidance**: Provide general health recommendations
- **Medical Context**: Use relevant medical knowledge for assessments

### Medication Information
- **Comprehensive Info**: Get uses, side effects, precautions, and interactions
- **Safety Focus**: Emphasize consulting healthcare providers
- **Educational Content**: Help users understand their medications

### Health Chat Interface
- **Medical Context**: Include relevant medical knowledge in responses
- **Category Filtering**: Focus on specific health areas
- **Medical Disclaimers**: Always include appropriate medical disclaimers

## 🧪 Testing

### Manual Testing

1. Start the server: `python main.py`
2. Open Streamlit: `streamlit run streamlit_app.py`
3. Add healthcare documents via the Health Knowledge interface
4. Test symptom assessment and medication lookup
5. Try health queries in the Chat Interface

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Get configuration
curl http://localhost:8000/config

# Get healthcare knowledge stats
curl http://localhost:8000/knowledge/stats

# Get available categories
curl http://localhost:8000/knowledge/categories
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenRouter API Key Error**
   - Ensure your `.env` file contains a valid `OPENROUTER_API_KEY`
   - Check that the API key has sufficient credits
   - Verify the model name is correct (e.g., `openai/gpt-4`)

2. **ChromaDB Connection Error**
   - Ensure the `healthcare_db` directory exists and is writable
   - Check file permissions

3. **Port Already in Use**
   - Change the port in `.env` file
   - Kill existing processes using the port

4. **Docker Issues**
   - Ensure Docker and Docker Compose are installed
   - Check that ports 8000 and 8501 are available

### Logs

```bash
# View Docker logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f mcp-server
docker-compose logs -f streamlit
```

## ⚠️ Medical Disclaimer

**IMPORTANT**: This AI assistant provides general health information only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for specific medical concerns.

The system includes:
- Medical disclaimers in all responses
- Emphasis on consulting healthcare providers
- Educational focus rather than diagnostic capabilities
- Source tracking for medical information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [OpenRouter](https://openrouter.ai/) for AI model access
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Streamlit](https://streamlit.io/) for the web interface
- Medical professionals and organizations for healthcare guidance 

## 🚀 Deploying on Railway

1. **Push your code to GitHub.**
2. **Go to [Railway](https://railway.app/)** and create a new project.
3. **Connect your GitHub repository** to Railway.
4. Railway will auto-detect the `Dockerfile` and build your app using it.
5. **Set environment variables** (such as `OPENAI_API_KEY`) in the Railway dashboard under the Variables tab.
6. **Deploy!** Railway will build and run your app. You will get a public URL once deployment is complete.

**Note:**
- The app will be served using Gunicorn for production reliability.
- The server will listen on the port provided by Railway via the `$PORT` environment variable.
- If you need a database, add it via Railway's Plugins and update your config accordingly. 