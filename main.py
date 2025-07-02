from flask import Flask, request, jsonify
import json
import requests
import os

app = Flask(__name__)

# 🔐 আপনার Dropbox Token
DROPBOX_TOKEN = "sl.u.AF0tz4u_uow9jp8FLM-0YEDIpnoQjrWLRA4fGhPpQOPJ5bviuwL9WoRLHo7DPK7W7ODRQ81VJxwDQb3wEb_369s8uXnG7d8mU9Q8lH8j_fjyz4kyHKgbgQ5HZaTduDgncvXNVsxCydiPZjBEcO6R6esIlObJps2BwETYswtFciOT-7H7obu3VB2SZ0oynC47e_BnX-_G-2fofXnxRACiRCCQRVGrw7O8rMSopDRPpbPbFtrtZV44w3MAmtGxFL8L9w8IG4EmjhEixoQGDytSMhnvDPsue-uxvSa5Jvvn9dORMVWLCoMK2vLnDH4RrNWm12iYWEx0dJNVKMjcC4PMfSMEdogvWlFUTbvJmL4OaRNiPL0vtcYKThWOtbtojJqzPvQjO-SO2K0B6JEDo6gLT4mg3T_5C3fLaZKktakV-Fenf5Vtd9Rdv8951ojkycRU3PEAo04HsPWchgZzk95UVDAwx52-jGJF6bwONzP_wORcIzAzOq7fKw5pueq59D_GUFDg517iWxW7y49qi12qU2jHgwPUtHPWZTONkY4hmcI07jQajOIwRxpgyqp0WmEqRYODsKSwgTXr-pqeJ5wCE6tzthM28O9ZpSKIVRtnZqodoKBgSsRmqQUQqFUv5Naze4ij1AdBKNBrEM2YhvdXWsELA2aTOgvDOwdODi3sgbOllsmrDzQt38HCe9RY8iDUF1Fy8Ewdh9yCI53QqIHqevk0AxxJFYLgosa7o9hmjQa3SV9m01Jwzs47SU6M3XoKRyCFnx9Fp1gOIItVT3Kqci5K40Ga6TJbhXBBWslz6xTj1m5lWP4xjo-e0tHgdjM6MVyyXZl94TFfFnUs3pj2Nr0DtQyWSO8L-gyZvG_ZAAE9A1C4wYJNnUMfP4FcKXlaF65O7HikGDEPY-Wl9J-e7WoRWjIsF4EkKYqITjnNe_mrTcUr3jI6Rdrh-40odfe9wzoc4uvtw8pyx9ICmiHepholZdqk-4zIVgCWFP_Qg9qNPoBEhZc55Ecmme_6IEJGuMu96PxCsgX3ozgpWE1xSHGPWI7i4iO3vJLV_CXSpcECVYw4y5IEYt8QOkYh1aVg9g9jGe6MTuUsfJvhHHBw212YxiJCoUo8A5dmLQ0E9QYBIf7IcdbYNApxvUWWQddR7fMLLPd7PxpNItsifY9K_fEK8Cf0pMUZX3N86REXmalWT4F85yQhHSNR_xljrzWUodwyxwmnitASpqoBZ36q0rTFCPyLF7bwvZWvYCXiwZPp4esOLTmT5jHz_Uo6zGu6K_aEGxWpf5xu06H0IYCMBjVHuvZ9ZLv4N3t3Q__AzoA9J-NUKQ6jHGXQuuT1g-cg9diKQy0Q3GorpLpMzRA4mLcPGs1u_ogzG6B0kqu5m4zfoP_ixkOSA5GK_FB5fyrakhOoI4ZyaXooywawtKWDPzVH"

# 🔄 JSON ফাইলের Dropbox পাথ
DROPBOX_FILE_PATH = "/admin_gui/licenses.json"

# 🔗 Dropbox API URLs
DROPBOX_UPLOAD_URL = "https://content.dropboxapi.com/2/files/upload"
DROPBOX_DOWNLOAD_URL = "https://content.dropboxapi.com/2/files/download"

HEADERS = {
    "Authorization": f"Bearer {DROPBOX_TOKEN}",
}

# 🔽 JSON ডাউনলোড
def download_json():
    headers = HEADERS.copy()
    headers["Dropbox-API-Arg"] = json.dumps({"path": DROPBOX_FILE_PATH})
    res = requests.post(DROPBOX_DOWNLOAD_URL, headers=headers)
    return json.loads(res.content)

# 🔼 JSON আপলোড
def upload_json(data):
    headers = HEADERS.copy()
    headers["Content-Type"] = "application/octet-stream"
    headers["Dropbox-API-Arg"] = json.dumps({
        "path": DROPBOX_FILE_PATH,
        "mode": "overwrite"
    })
    requests.post(DROPBOX_UPLOAD_URL, headers=headers, data=json.dumps(data).encode())

# 🔑 License activate API
@app.route("/activate", methods=["POST"])
def activate():
    req = request.get_json()
    license_key = req.get("license_key")

    data = download_json()

    for lic in data["licenses"]:
        if lic["license_key"] == license_key:
            lic["used"] = lic.get("used", 0) + 1
            upload_json(data)
            return jsonify({"success": True, "message": "✅ used updated"})

    return jsonify({"success": False, "message": "❌ License not found"}), 400

# ✅ Render server এ run করার জন্য
@app.route("/", methods=["GET"])
def home():
    return "✅ License Server is Running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
