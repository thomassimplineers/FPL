from flask import Flask

# Skapa Flask-applikationen
app = Flask(__name__)

# En enkel test-route för att se om backend fungerar
@app.route('/test', methods=['GET'])
def test():
    return "Hello World! Backend fungerar korrekt"

# Kör applikationen (endast för lokal utveckling, inte i produktionsmiljö)
if __name__ == '__main__':
    app.run(debug=True)
