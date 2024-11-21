from flask import Flask, send_file
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

# Kör applikationen (endast för lokal utveckling, inte i produktionsmiljö)
if __name__ == '__main__':
    app.run(debug=True)
