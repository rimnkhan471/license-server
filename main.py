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
    return "License Server is Running ✅"

@app.route("/add_or_edit_license", methods=["POST"])
def add_or_edit_license():
    data = request.get_json()
    license_key = data.get("key")
    expiry = data.get("expiry")

    licenses = load_licenses()

    # পুরনো লাইসেন্স মুছে ফেলা
    licenses["licenses"] = [l for l in licenses["licenses"] if l["license_key"] != license_key]

    # নতুন লাইসেন্স যোগ
    licenses["licenses"].append({
        "license_key": license_key,
        "expires": expiry,
        "max_devices": 1,
        "devices": [],
        "blocked": False
    })

    save_licenses(licenses)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
