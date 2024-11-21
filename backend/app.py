from flask import Flask, request, jsonify, send_file, abort
import os
import openai
from flask_cors import CORS
import pandas as pd
from io import BytesIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Skapa Flask-applikationen
app = Flask(__name__)

# Uppdaterad CORS-konfiguration
CORS(app, resources={r"/*": {"origins": "https://thomassimplineers.github.io"}},
     expose_headers="Authorization",
     supports_credentials=False)

# Rate Limiting för att förhindra missbruk av API:t
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Hämta API-nycklar från miljövariabler
openai.api_key = os.getenv('OPENAI_API_KEY')
backend_api_key = os.getenv('BACKEND_API_KEY')

# Ladda in data från CSV-fil
player_data = pd.read_csv('data/players_raw.csv')

# Route för att ställa frågor till GPT
@ask_gpt.before_request
def before_ask_gpt():
    if request.method == 'OPTIONS':
        # Tillåt OPTIONS-förfrågningar utan autentisering
        return
    # Kontrollera API-nyckel från förfrågan
    request_api_key = request.headers.get('Authorization')
    if request_api_key != backend_api_key:
        return abort(401)  # Unauthorized

    # Bearbeta GPT-förfrågan
    data = request.get_json()
    question = data.get('question', '')
    prompt = f"Analysera följande data och besvara frågan: {question}\nData: {player_data.head(5).to_json(orient='records')}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'answer': answer})

# Route för att ladda ner Excel-fil (exempel på annan route)
@app.route('/download_excel', methods=['GET'])
@limiter.limit("5 per minute")
def download_excel():
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    player_data.to_excel(writer, index=False)
    writer.save()
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        attachment_filename='player_data.xlsx'
    )

# Kör applikationen (endast för lokal utveckling, inte i produktionsmiljö)
if __name__ == '__main__':
    app.run(debug=True)
