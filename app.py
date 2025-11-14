# build a small python rest Api using flask with 2 end point
# /status--> ok
# /sum which can sum 2 number a and b

# also have to perfomr pytest for both the end point using request module
# test_api.py
# app.py
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Flask API running. Use /status or /sum?a=1&b=2"}), 200

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"message": "ok"}), 200

@app.route("/sum", methods=["GET"])
def sum_numbers():
    a_raw = request.args.get("a", None)
    b_raw = request.args.get("b", None)

    if a_raw is None or b_raw is None:
        return jsonify({"error": "Missing parameters 'a' or 'b'. Usage: /sum?a=1&b=2"}), 400

    try:
        a = float(a_raw)
        b = float(b_raw)
    except ValueError:
        return jsonify({"error": "Parameters must be numbers"}), 400

    result = a + b
    if a.is_integer() and b.is_integer():
        result = int(result)

    return jsonify({"sum": result}), 200

@app.route("/favicon.ico")
def favicon():
    path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    if os.path.exists(path):
        return send_from_directory(os.path.dirname(__file__), "favicon.ico")
    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True)
