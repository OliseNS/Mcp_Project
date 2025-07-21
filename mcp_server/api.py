from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from .agent import HealthcareAgent
from .config import Config
import os

app = Flask(__name__)
CORS(app)

agent = HealthcareAgent()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "Healthcare MCP Server"})

@app.route("/query", methods=["POST"])
def process_query():
    data = request.get_json()
    try:
        # Store user context as a document if provided
        user_context = data.get("user_context")
        if user_context:
            agent.add_healthcare_knowledge([
                {
                    "text": user_context,
                    "metadata": {"source": "user_context", "type": "user_submission"},
                    "id": None
                }
            ])
        result = agent.process_query(
            user_input=data.get("query"),
            search_k=data.get("search_k", 5),
            include_context=data.get("include_context", True),
            category=data.get("category"),
            user_context=user_context
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/assess-symptoms", methods=["POST"])
def assess_symptoms():
    data = request.get_json()
    try:
        result = agent.assess_symptoms(
            symptoms=data.get("symptoms", []),
            search_k=data.get("search_k", 5)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/medication-info", methods=["POST"])
def get_medication_info():
    data = request.get_json()
    try:
        result = agent.get_medication_info(
            medication_name=data.get("medication_name"),
            search_k=data.get("search_k", 5)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/knowledge/add", methods=["POST"])
def add_documents():
    data = request.get_json()
    try:
        documents = []
        for doc in data.get("documents", []):
            documents.append({
                "text": doc.get("text"),
                "metadata": doc.get("metadata", {}),
                "id": doc.get("doc_id")
            })
        result = agent.add_healthcare_knowledge(documents)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/knowledge/stats", methods=["GET"])
def get_knowledge_stats():
    try:
        return jsonify(agent.get_healthcare_stats())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/knowledge/categories", methods=["GET"])
def get_categories():
    try:
        stats = agent.get_healthcare_stats()
        if stats.get("status") == "success":
            return jsonify({
                "status": "success",
                "categories": stats.get("categories", []),
                "category_counts": stats.get("category_counts", {})
            })
        else:
            return jsonify({"error": stats.get("error", "Unknown error")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/knowledge/category/<category>", methods=["GET"])
def get_documents_by_category(category):
    try:
        return jsonify(agent.get_documents_by_category(category))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/knowledge/clear", methods=["DELETE"])
def clear_knowledge():
    try:
        return jsonify(agent.clear_knowledge())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/knowledge/search", methods=["POST"])
def search_knowledge():
    data = request.get_json()
    try:
        if data.get("category"):
            return jsonify(agent.search_by_category(data["query"], data["category"], data.get("n_results", 5)))
        else:
            results = agent.vector_db.search(data["query"], n_results=data.get("n_results", 5))
            return jsonify({
                "status": "success",
                "query": data["query"],
                "results": results,
                "count": len(results)
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/conversation", methods=["POST"])
def conversation():
    data = request.get_json()
    try:
        result = agent.chat_conversation(
            messages=data.get("messages", []),
            search_k=data.get("search_k", 5),
            user_context=data.get("user_context")
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "model_name": Config.MODEL_NAME,
        "temperature": Config.TEMPERATURE,
        "max_tokens": Config.MAX_TOKENS,
        "chroma_db_path": Config.CHROMA_DB_PATH,
        "healthcare_collection": Config.HEALTHCARE_COLLECTION,
        "host": Config.HOST,
        "port": Config.PORT,
        "medical_disclaimer": Config.MEDICAL_DISCLAIMER
    })

@app.get("/example-contexts")
def get_example_contexts():
    """Serve example contexts from a JSON file."""
    import json
    example_file = os.path.join(os.path.dirname(__file__), "example_contexts.json")
    if not os.path.exists(example_file):
        return {"examples": []}
    with open(example_file, "r", encoding="utf-8") as f:
        try:
            examples = json.load(f)
        except Exception:
            examples = []
    return {"examples": examples}

def run_server():
    try:
        Config.validate()
        app.run(host=Config.HOST, port=Config.PORT, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        return False
    return True

if __name__ == "__main__":
    run_server() 