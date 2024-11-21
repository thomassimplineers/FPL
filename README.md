FPL Analyzer
En webbapplikation som analyserar Fantasy Premier League-data och ger intelligenta insikter genom GPT-integration.

Innehållsförteckning
Introduktion
Funktioner
Demonstration
Installation
Användning
Arkitektur
Automatiska Uppdateringar
Teknologier som Används
Bidra
Licens
Kontakt
Tack till
Introduktion
FPL Analyzer är en webbapplikation designad för Fantasy Premier League-entusiaster. Den kombinerar kraften i dataanalys med AI genom att integrera OpenAI:s GPT för att ge användarna djupa insikter och rekommendationer baserat på aktuell spelarstatistik.

Funktioner
Dataanalys av spelare:
Beräkning av Total Score.
Beräkning av VFM (Value for Money).
GPT-integration:
Ställ frågor om spelarprestationer och få intelligenta svar.
Få personliga rekommendationer för lagutveckling.
Dataexport:
Ladda ner detaljerad spelarstatistik som en Excel-fil.
Automatiska datauppdateringar:
Veckovisa uppdateringar av spelarstatistik via GitHub Actions.
Demonstration
Länk till live-demonstration: FPL Analyzer

Installation
Följ dessa steg för att sätta upp projektet lokalt eller för att bidra:

Förutsättningar
Git
Python 3.x
En OpenAI API-nyckel
Heroku CLI (för deployment)
Klona Repositoriet
bash
Copy code
git clone https://github.com/<ditt-användarnamn>/fpl-analyzer.git
cd fpl-analyzer
Backend Installation
Navigera till backend-mappen:

bash
Copy code
cd backend
Skapa en virtuell miljö och aktivera den:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Installera beroenden:

bash
Copy code
pip install -r requirements.txt
Ställ in miljövariabler:

Skapa en fil .env och lägg till din OpenAI API-nyckel:

makefile
Copy code
OPENAI_API_KEY=din-api-nyckel-här
Kör applikationen lokalt:

bash
Copy code
flask run
Frontend Installation
Frontend är hostad på GitHub Pages och kräver ingen lokal installation. För att göra ändringar:

Navigera till rotmappen:

bash
Copy code
cd ..
Redigera index.html, app.js, och styles.css enligt behov.

Användning
Använda Webbapplikationen
Besök webbplatsen:

plaintext
Copy code
https://<ditt-användarnamn>.github.io/fpl-analyzer
Ladda ner Spelardata:

Klicka på knappen "Ladda ner Spelardata" för att få en Excel-fil med aktuell spelarstatistik.
Ställ frågor till GPT:

Skriv in din fråga i textfältet och klicka på "Fråga GPT" för att få ett AI-genererat svar baserat på den senaste datan.
Exempel på Frågor att Ställa
"Vilken anfallare erbjuder bäst värde för pengarna just nu?"
"Vilka mittfältare har presterat bäst de senaste fem matcherna?"
"Rekommendera tre försvarare med hög Total Score."
Arkitektur
Frontend:
Hostad på GitHub Pages.
Byggd med HTML, CSS och JavaScript.
Backend:
Hostad på Heroku.
Flask-applikation som hanterar API-förfrågningar, databehandling med Pandas, och GPT-integration via OpenAI API.
Automatiserade Uppdateringar:
GitHub Actions används för att hämta den senaste spelarstatistiken en gång i veckan.
Automatiska Uppdateringar
Datauppdatering:
Ett GitHub Actions-workflow (update_data.yml) körs varje vecka för att automatiskt uppdatera spelarstatistiken från vaastav/Fantasy-Premier-League.
Deployment:
Heroku är konfigurerat för att automatiskt deploya den uppdaterade applikationen efter varje uppdatering.
Teknologier som Används
Python & Flask - Backend-ramverk
Pandas - Databehandling
OpenAI GPT-3 - AI-driven textgenerering
JavaScript, HTML, CSS - Frontend-utveckling
GitHub Pages - Hosting av frontend
Heroku - Hosting av backend
GitHub Actions - CI/CD och automatiska uppdateringar
Bidra
Bidrag är välkomna! Följ dessa steg för att bidra till projektet:

Forka repositoriet.

Skapa en ny gren för din funktion eller buggfix:

bash
Copy code
git checkout -b feature/ny-funktion
Gör dina ändringar och commit:a:

bash
Copy code
git commit -m "Lade till ny funktion"
Push:a till din forkade repositori:

bash
Copy code
git push origin feature/ny-funktion
Skapa en Pull Request på GitHub.

Licens
Detta projekt är licensierat under MIT-licensen.

Kontakt
Projektunderhållare: Ditt Namn
GitHub: @ditt-användarnamn
Tack till
vaastav/Fantasy-Premier-League för den omfattande spelarstatistiken.
OpenAI för GPT-modellen.
Alla öppna källkodsbidragsgivare och communityn.
