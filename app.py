from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import marqo
from index_data import setup_application
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

app = Flask(__name__)

URL = "http://localhost:8882"
CLIENT = marqo.Client(url=URL)
INDEX_NAME = os.getenv("MARQO_INDEX_NAME", None)

DEVICE = os.getenv("MARQO_DEVICE", "cpu")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["search"]
        return redirect(url_for("search_results", query=query))
    return render_template("index.html")


@app.route("/search_results", methods=["POST"])
def search_results():
    data = request.get_json()
    search_query = data["search"]
    themes = data["themes"]
    negs = data["negatives"]

    query_weights = {
        search_query: 1.0,
    }

    if themes:
        query_weights[themes] = 0.75

    if negs:
        query_weights[negs] = -1.1

    results = CLIENT.index(INDEX_NAME).search(query_weights, device=DEVICE, limit=12)

    hits = results["hits"]

    return jsonify(hits)


if __name__ == "__main__":
    indexes = {index.index_name for index in CLIENT.get_indexes()["results"]}
    if INDEX_NAME not in indexes:
        setup_application()
    app.run(debug=True)
