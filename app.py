from flask import Flask, render_template
import json

app = Flask(__name__)

LOG_FILE = "user_logs.json"

@app.route('/')
def index():
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except Exception:
        logs = []
    return render_template("logs.html", logs=logs)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
