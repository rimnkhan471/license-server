from flask import Flask, request, jsonify
import json
import requests
import os

DROPBOX_TOKEN = os.environ.get("DROPBOX_TOKEN")
DROPBOX_PATH = "/admin_gui/licenses.json"

app = Flask(__name__)

def download_json():
    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Dropbox-API-Arg": json.dumps({ "path": DROPBOX_PATH }),
    }
    response = requests.post("https://content.dropboxapi.com/2/files/download", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Dropbox Download Error:", response.text)
        return None

def upload_json(data):
    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": json.dumps({
            "path": DROPBOX_PATH,
            "mode": "overwrite",
            "mute": True
        })
    }
    response = requests.post(
        "https://content.dropboxapi.com/2/files/upload",
        headers=headers,
        data=json.dumps(data, indent=4).encode("utf-8")
    )
    return response.status_code == 200

@app.route("/update_used", methods=["POST"])
def update_used():
    req = request.get_json()
    key = req.get("license_key", "").strip()

    if not key:
        return jsonify({"success": False, "error": "Missing license key"}), 400

    data = download_json()
    if not data:
        return jsonify({"success": False, "error": "Could not load licenses"}), 500

    found = False
    for lic in data["licenses"]:
        if lic["license_key"] == key:
            lic["used"] = lic.get("used", 0) + 1
            found = True
            break

    if not found:
        return jsonify({"success": False, "error": "License key not found"}), 404

    if upload_json(data):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Upload failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)