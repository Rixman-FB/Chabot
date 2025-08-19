import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# ... andere Importe
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS # 1. Importieren
from dotenv import load_dotenv


# .env-Datei laden, um den API-Key zugänglich zu machen
load_dotenv()

# Flask-App initialisieren
app = Flask(__name__)
CORS(app) # 2

# Gemini API konfigurieren
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except AttributeError as e:
    print("Fehler: Der GEMINI_API_KEY wurde nicht gefunden. Stellen Sie sicher, dass er in der .env-Datei gesetzt ist.")
    exit()

# Das Gemini-Modell auswählen
model = genai.GenerativeModel('gemini-1.5-flash') # Oder ein anderes passendes Modell

# Route für die Hauptseite, die das E-Learning-Modul anzeigt
@app.route('/')
def index():
    return render_template('index.html')

# Route für die Auswertung, die vom Frontend aufgerufen wird
@app.route('/evaluate', methods=['POST'])
def evaluate_text():
    # Daten aus der Anfrage des Frontends auslesen
    data = request.get_json()
    if not data or 'prompt' not in data or 'answer' not in data:
        return jsonify({'error': 'Ungültige Anfrage. "prompt" und "answer" sind erforderlich.'}), 400

    user_prompt = data['prompt']
    learner_answer = data['answer']

    # Den vollständigen Prompt für Gemini zusammenstellen
    full_prompt = f"{user_prompt}\n\nAntwort des Lernenden:\n\"\"\"\n{learner_answer}\n\"\"\""

    try:
        # Anfrage an die Gemini API senden
        response = model.generate_content(full_prompt)

        # Die Antwort von Gemini als JSON an das Frontend zurücksenden
        return jsonify({'evaluation': response.text})

    except Exception as e:
        # Fehlerbehandlung
        return jsonify({'error': f'Ein Fehler ist aufgetreten: {str(e)}'}), 500

# Den Server starten
if __name__ == '__main__':
    app.run(debug=True)