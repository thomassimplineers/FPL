from flask import Flask, request, jsonify, send_file, abort
import os
import openai
from flask_cors import CORS
import pandas as pd
from io import BytesIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Tillåt alla domäner temporärt för att felsöka CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]  # Gräns på antalet förfrågningar per användare
)

# Sätt API-nycklar
openai.api_key = os.getenv('OPENAI_API_KEY')
backend_api_key = os.getenv('BACKEND_API_KEY')

# Ladda data
player_data = pd.read_csv('data/players_raw.csv')

@app.route('/ask_gpt', methods=['POST'])
@limiter.limit("10 per minute")  # Ytterligare begränsning per endpoint
def ask_gpt():
    # Kontrollera API-nyckel från förfrågan
    request_api_key = request.headers.get('Authorization')
    if request_api_key != backend_api_key:
        return abort(401)  # Unauthorized

    data = request.get_json()
    question = data.get('question', '')
    # Bearbeta frågan och data
    prompt = f"Analysera följande data och besvara frågan: {question}\nData: {player_data.head(5).to_json(orient='records')}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    answer = response.choices[0].text.strip()
    return jsonify({'answer': answer})

@app.route('/download_excel', methods=['GET'])
@limiter.limit("5 per minute")  # Begränsning på antalet nedladdningar
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

if __name__ == '__main__':
    app.run(debug=True)
