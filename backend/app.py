from flask import Flask, request, jsonify
from flask_cors import CORS
from search import search_duckduckgo

app = Flask(__name__)
CORS(app)

@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query required"}), 400

    results = search_duckduckgo(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
