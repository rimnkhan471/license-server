# Excel License Server

This is a simple Node.js license validation API for Excel VBA.

## Endpoint

`GET /validate?key=YOUR_LICENSE_KEY`

### Response:
- `VALID` = License is accepted
- `INVALID` = License is invalid, expired, blocked, or limit exceeded

## Deploy using Railway
1. Go to [https://railway.app](https://railway.app)
2. Click "New Project" > "Deploy from GitHub Repo"
3. Select this repository
4. Done! ✅