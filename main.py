from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
LICENSE_FILE = "licenses.json"

def load_data():
    if not os.path.exists(LICENSE_FILE):
        return {}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return "✅ License Server is Running on Render!"

@app.route("/add_or_edit_license", methods=["POST"])
def add_or_edit():
    key = request.json.get("key")
    expiry = request.json.get("expiry")

    data = load_data()
    if key not in data:
        data[key] = {"pc_ids": [], "expiry": expiry}
    else:
        data[key]["expiry"] = expiry

    save_data(data)
    return jsonify({"status": "success"})

@app.route("/check_license", methods=["GET"])
def check():
    key = request.args.get("key")
    pcid = request.args.get("pcid")

    data = load_data()
    lic = data.get(key)

    if not lic:
        return jsonify({"status": "invalid"})

    if pcid in lic["pc_ids"]:
        return jsonify({"status": "valid", "expiry": lic["expiry"]})

    if len(lic["pc_ids"]) < 2:
        lic["pc_ids"].append(pcid)
        save_data(data)
        return jsonify({"status": "valid", "expiry": lic["expiry"]})

    return jsonify({"status": "limit"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)