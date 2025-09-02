from flask import Flask, render_template, request, jsonify
import os, requests, base64
from datetime import datetime

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
FORM_PASSWORD = os.getenv("FORM_PASSWORD")
BRANCH = "main"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if data.get("password") != FORM_PASSWORD:
        return jsonify({"message": "Incorrect password"}), 403

    content = {
        "name": data.get("name"),
        "age": data.get("age"),
        "occupation": data.get("occupation"),
        "submitted_at": datetime.utcnow().isoformat()
    }

    filename = f"data/submission_{datetime.utcnow().timestamp()}.json"
    encoded = base64.b64encode(bytes(str(content), "utf-8")).decode("utf-8")

    response = requests.put(
        f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}",
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        },
        json={
            "message": "New submission",
            "content": encoded,
            "branch": BRANCH
        }
    )

    if response.ok:
        return jsonify({"message": "Submission successful!"})
    else:
        return jsonify({"message": "GitHub error", "details": response.json()}), 500

if __name__ == "__main__":
    app.run()
