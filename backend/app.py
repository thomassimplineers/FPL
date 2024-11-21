from flask import Flask, send_file, request, jsonify
import os
import pandas as pd
from io import BytesIO
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Skapa Flask-applikationen
app = Flask(__name__)

# Uppdaterad CORS-konfiguration för att tillåta frontend-anslutningar från GitHub Pages
CORS(app, resources={r"/*": {"origins": "https://thomassimplineers.github.io"}})

# Rate Limiting för att förhindra missbruk av API:t
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    headers_enabled=True
)

# Ladda in data från CSV-fil
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'players_raw.csv')

try:
    player_data = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    player_data = pd.DataFrame()  # Tom DataFrame om datafilen saknas

# Funktion för att analysera spelardata och beräkna total poäng och VFM
def analyze_player_data(player_data):
    if player_data.empty:
        return player_data

    # Lägg till VFM-kolumn (Value for Money)
    player_data['VFM'] = player_data['total_points'] / (player_data['now_cost'] / 10)  # VFM = Total poäng per miljon

    # Sortera spelare efter VFM för att hitta de bästa spelarna inom budget
    player_data = player_data.sort_values(by='VFM', ascending=False)

    return player_data

# Route för att ladda ner analyserad Excel-fil
@app.route('/download_analysis', methods=['GET'])
@limiter.limit("5 per minute")
def download_analysis():
    if player_data.empty:
        return "Data saknas för att generera Excel-fil", 404

    # Analysera spelardata
    analyzed_data = analyze_player_data(player_data)

    # Skapa Excel-fil från analyserad data
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    analyzed_data.to_excel(writer, index=False, sheet_name='Spelaranalys')
    writer.save()
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        attachment_filename='analyserad_spelardata.xlsx'
    )

# Kör applikationen (endast för lokal utveckling, inte i produktionsmiljö)
if __name__ == '__main__':
    app.run(debug=True)
