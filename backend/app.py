from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "backend_api"})

@app.route("/upload", methods=["POST"])
def upload():
    return jsonify({"error": "Service endpoint initialized, but logic is not yet implemented."}, 501)

if __name__ == "__main__":
    app.run(debug=True, port=5000)