from flask import Flask, request, jsonify
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

app = Flask(__name__)

# Define ChromaDB storage path
CHROMA_PATH = r"C:\Users\hp\Desktop\chatbot\chroma_db"

# Load the embedding function
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the stored vector store
vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function
)

# Create a retriever for similarity search
retriever = vector_store.as_retriever(search_kwargs={"k": 5})  # Retrieve top 5 matches

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is working!"})

@app.route("/search", methods=["POST"])
def search():
    try:
        # Get user query from request JSON
        data = request.get_json()
        user_query = data.get("query")

        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        # Perform similarity search with scores
        retrieved = vector_store.similarity_search_with_score(user_query, k=5)

        min_score = min(score for _, score in retrieved)
        max_score = max(score for _, score in retrieved)

        # Extract courses with scores
        matches = []
        seen_courses = set()  # To remove duplicates

        for doc, score in retrieved:
            course_name = doc.page_content.strip()

            if course_name not in seen_courses:
                seen_courses.add(course_name)  # Track seen courses

                # Normalize score (invert distance so higher means better match)
                normalized_score = 1 - ((score - min_score) / (max_score - min_score + 1e-6))

                matches.append({
                    "course": course_name,
                    "metadata": doc.metadata,
                    "score": round(normalized_score, 4)  # Round to 4 decimal places
                })

        return jsonify({"query": user_query, "results": matches[:5]})  # Limit to top 5

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


