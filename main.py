from flask import Flask, request, jsonify
import json
import requests
import os

# ✅ Dropbox Token & Path (TOKEN HARDCODED)
DROPBOX_TOKEN = "sl.u.AF2lGO7XFwL4T0L0insEgijAjIem7VeIi3hS7VwMuRIphiHiunaSIv-3FEb4B5jowW0rzgTL1T6AiQUKBE0fTPBAbf6rpkL0MYWPM_JJYCxUQKXx1U7-isDZbiIVFyNm0P-Lngt0vr7Ci_li8oCPz0Crz6dLvx7q57mPYdY7phqkFPi6EHMFMmjRZH63DbdBzI1Tdv3jGq0IXfAjyIDu-dBwswkf-eA2xWGN-FX37oUbEeSP9PrZoZ-DJ80R9_60RjxowL5gfLO_h21hb6z7E02HkiI-c62SFGfGFnIEHfcNrr3qpGa4-Nm3Nd43LwtYT1qqZxXZQryekh9RmbY7aNdZoy5cMDxEmFzD6bN8zmxnsCOVmSey9vyRUtn5oA6QmMYpvmEWH5Ud8d10AODZinScIzXNjKAjSBfDlkOxp6fEPmlQlklgGp2tQAUFu53CweQv1hJJ8q26MWwFc2NOs23yLSGTqebkG-fi9zG85YTglA444akHND6YzUMSJogYBtE9LIa2wbdMqssjS21thuYzrH2cd_oyIuVjjRDh-qi8Btt4m86XHs_NgjmMvlcxuPnPNFms2S8XBl5vvYV-MKM8BTNInZfimqHPVM2LDKyiBfo8K55Ctg7sznDqMmFxigZbi4HS0w2W-dB-Jymx2YedQ4BNeFoLo9ubT-mlO2cJHH56_827WyVNlavDWGWeQ2uErSKIvxhq8JksnvwXbgO5C2--L7fU-zsM5nh3yYP87ouE0h_rX94wRD6VTVpQQO7XKMdpaB87atzZZKwFWVjJCt-VNscdbzsqfD1Y_NIlk7hikqK-TJuBS5cjwdVKJB7Ugdbo2vYETlFk_ZyTqoo88Uh2B2KOqnmHs3U4tcGX9C67YoOzSxbMCBYejz7UgovIJqTQXhecuObEMffvqfNn6kv7aPJDImRiJ019UZz8WSBaZQo3k2nA43YjmKpJkCzRUQqLQQvcPbvBGH6r_RiVo7waiaErWm0IMcazs2w5M9ebj_qGyDGosiBkel8jhIUbf4fLKhOYpZcyoaPp7_dmrICy5W7GQ7PZwv9peyi52i4CxGAzestz0O6KOzJ8sAqbRPO43tMTK4r-avcGr0OyoJvxx5e5hK0RjXN3fi0_NM0xzLyXqrvDlxApF1Y95E96qoiqNno8VYe_loeqX6ob9KpQVcLIXMdl6P3fnvsUJCxWdbdYEGeHjr0f2YpAKsYPbsYhfHb4354F9Pa9TAp5jXLawf_0sAhQH0F0Ek0ktrjxmXSAyHqNUmShrOoY7pGuGMaEyuqCLEn9GqgB4h5XE_YKUBIO1vZv_WIc27dri2OK17FE9s7TLlEubTbvqoGkDTAaadi9fG4nopKIBY1-ZerslXgb_wGfv69S2bDLzOWwgcrJe-daQhUVuFWoI-njlLkxzqpXsihs3VFKG7oq"
DROPBOX_PATH = "/admin_gui/licenses.json"

app = Flask(__name__)

# ✅ Download licenses.json from Dropbox
def download_json():
    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Dropbox-API-Arg": json.dumps({
            "path": DROPBOX_PATH
        }),
    }
    response = requests.post("https://content.dropboxapi.com/2/files/download", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Dropbox Download Error:", response.text)
        return None

# ✅ Upload licenses.json to Dropbox
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

# ✅ POST API: /update_used
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

# ✅ Run server on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
