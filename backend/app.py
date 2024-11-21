from flask import Flask, send_file, request, jsonify
import os
import pandas as pd
from io import BytesIO
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Skapa Flask-applikationen
app = Flask(__name__)

# Uppdaterad CORS-konfiguration
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

# Route för att ladda ner Excel-fil
@app.route('/download_excel', methods=['GET'])
@limiter.limit("5 per minute")
def download_excel():
    if player_data.empty:
        return "Data saknas f\u00f6r att generera Excel-fil", 404

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

# Route för att beräkna bästa laget inom budget
@app.route('/optimize_team', methods=['POST'])
def optimize_team():
    if player_data.empty:
        return jsonify({"error": "Ingen spelar-data tillgänglig"}), 404
    
    data = request.get_json()
    budget = data.get('budget', 100.0)  # Standardbudget är 100 miljoner

    # Beräkna VFM för varje spelare (Poäng per miljon)
    player_data['VFM'] = player_data['total_points'] / player_data['now_cost']

    # Välj spelare baserat på budget och VFM
    selected_players = []
    remaining_budget = budget * 10  # Budgeten är i miljoner (konvertera till samma enhet som 'now_cost')
    
    # Sortera spelare efter VFM
    sorted_players = player_data.sort_values(by='VFM', ascending=False)

    for _, player in sorted_players.iterrows():
        if player['now_cost'] <= remaining_budget and len(selected_players) < 15:
            selected_players.append(player)
            remaining_budget -= player['now_cost']

    # Skapa en lista över valda spelare
    selected_players_data = pd.DataFrame(selected_players)

    # Omvandla till JSON-format för frontend
    result = selected_players_data.to_dict(orient='records')
    return jsonify({"team": result, "remaining_budget": remaining_budget / 10})  # Återställa budgeten till miljoner

# Kör applikationen (endast för lokal utveckling, inte i produktionsmiljö)
if __name__ == '__main__':
    app.run(debug=True)
