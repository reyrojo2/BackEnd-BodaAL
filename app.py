from flask import Flask, request, jsonify
from utils import generar_token, validar_token
from datetime import datetime
import gspread
import json
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
load_dotenv()
# Google Sheets setup
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
cred_raw = os.getenv("GOOGLE_CREDS")
creds = json.loads(cred_raw)
creds["private_key"] = creds["private_key"].replace("\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
client = gspread.authorize(creds)
sheet = client.open("AsistenciaBoda").sheet1


@app.route("/ping")
def ping():
    return "pong", 200


@app.route("/get-token")
def get_token():
    ts, tk = generar_token()
    return jsonify({"timestamp": ts, "token": tk})


@app.route("/asistencia", methods=["POST"])
def asistencia():
    data = request.json
    if not validar_token(data.get("timestamp"), data.get("token")):
        return jsonify({"error": True, "desc": "Token inválido o expirado"}), 403

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row(
        [
            timestamp,
            data.get("asistencia"),
            data.get("nombre"),
            data.get("celular"),
            data.get("correo"),
        ]
    )
    return jsonify({"error": False})


if __name__ == "__main__":
    app.run(debug=True)
