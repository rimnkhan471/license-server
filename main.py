from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LICENSE_FILE = "licenses.json"

def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        return {"licenses": []}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return "✅ License Server is Running"

@app.route("/add_or_edit_license", methods=["POST"])
def add_or_edit_license():
    try:
        data = request.get_json()
        license_key = data.get("key")
        expiry = data.get("expiry")

        if not license_key or not expiry:
            return jsonify({"status": "error", "message": "Missing key or expiry"}), 400

        licenses = load_licenses()
        licenses["licenses"] = [l for l in licenses["licenses"] if l["license_key"] != license_key]
        licenses["licenses"].append({
            "license_key": license_key,
            "expires": expiry,
            "max_devices": 1,
            "devices": [],
            "blocked": False
        })

        save_licenses(licenses)
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0")
