from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

HIGH_SCORES_FILE = os.path.join(os.path.dirname(__file__), "high_scores.json")


def load_scores():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, "r") as f:
            return json.load(f)
    return []


def save_scores(scores):
    with open(HIGH_SCORES_FILE, "w") as f:
        json.dump(scores, f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scores", methods=["GET"])
def get_scores():
    scores = load_scores()
    return jsonify(scores[:10])


@app.route("/api/scores", methods=["POST"])
def post_score():
    data = request.get_json()
    if not data or "name" not in data or "score" not in data:
        return jsonify({"error": "Invalid data"}), 400

    name = str(data["name"])[:20].strip()
    try:
        score = int(data["score"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid score"}), 400

    if not name or score < 0:
        return jsonify({"error": "Invalid data"}), 400

    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]
    save_scores(scores)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
