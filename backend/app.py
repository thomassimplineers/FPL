from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import pandas as pd
from io import BytesIO
import openai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://thomassimplineers.github.io"}})

# Sätt OpenAI API-nyckel
openai.api_key = os.getenv('OPENAI_API_KEY')

# Ladda data
player_data = pd.read_csv('data/players_raw.csv')

@app.route('/ask_gpt', methods=['POST'])
def ask_gpt():
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
def download_excel():
    # Utför nödvändig databehandling här (t.ex. beräkna Total Score, VFM)
    # Här använder vi bara den befintliga datan som exempel
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
