"""
CureBridge Flask Server & REST API
Author: Ateeq Wahlan (https://wahlanos.com | https://github.com/ateeq-wahlan)
"""
from flask import Flask, render_template, request, jsonify
from curebridge_engine import CureBridgeEngine

app = Flask(__name__)
engine = CureBridgeEngine("model.pkl")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    payload = request.get_json(force=True) or {}
    features = payload.get("features", [34, 23.4, 118, 92, 97, 7.5, 1, 1, 0, 0, 0, 0, 0, 0, 2])
    result = engine.predict_profile(features)
    return jsonify({"status": "ok", "prediction": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
