from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

LICENSE_FILE = "licenses.json"

# লাইসেন্স লোড
def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        return {"licenses": []}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

# লাইসেন্স সেভ
def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# রুট চেক (GET)
@app.route("/")
def home():
    return "License Server is Running ✅"

# লাইসেন্স ADD বা UPDATE (POST)
@app.route("/add_or_edit_license", methods=["POST"])
def add_or_edit_license():
    try:
        data = request.get_json()
        license_key = data.get("key")
        expiry = data.get("expiry")

        if not license_key or not expiry:
            return jsonify({"status": "error", "message": "Missing key or expiry"}), 400

        licenses = load_licenses()

        # একই key থাকলে আগেরটা মুছে ফেলা
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

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ✅ Render-এ চলার জন্য port বাদ
if __name__ == "__main__":
    app.run(host="0.0.0.0")
