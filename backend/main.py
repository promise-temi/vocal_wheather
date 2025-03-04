from test_main import meteo_response
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)

# Autoriser les requêtes CORS pour toutes les origines avec support des credentials.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

class Session:
    def __init__(self, latitude="", longitude=""):
        # Initialisation des coordonnées de session avec des valeurs par défaut
        self.latitude = latitude
        self.longitude = longitude

# Objet global pour stocker les coordonnées de localisation actuelles
session = Session()

@app.route('/localisation', methods=['POST', 'OPTIONS'])
def localisation():
    """
    Endpoint pour recevoir et stocker la localisation (latitude et longitude).
    
    Méthode POST:
      Reçoit un JSON contenant les clés 'latitude' et 'longitude' et met à jour la session.
    
    Méthode OPTIONS:
      Répond à la requête de préflight CORS.
    """
    if request.method == "OPTIONS":
        return jsonify({"message": "Préflight CORS réussi"}), 200

    try:
        data = request.get_json()
        # Affichage des coordonnées reçues pour vérification
        print(data['longitude'])
        print(data['latitude'])
        # Mise à jour de l'objet session avec les nouvelles coordonnées
        session.latitude = data['latitude']
        session.longitude = data['longitude']
        return jsonify({'message': 'bien recu'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': "Une erreur s'est produite"}), 500

@app.route('/save-text', methods=['POST', 'OPTIONS'])
def save_text():
    """
    Endpoint pour traiter le texte de commande vocale.
    
    Méthode POST:
      - Reçoit un JSON avec la clé "text" contenant le texte reconnu.
      - Extrait les informations (dates, ville) du texte et récupère les données météo associées.
      - Nettoie et formate les résultats pour une réponse JSON.
    
    Méthode OPTIONS:
      Répond à la requête de préflight CORS.
    """
    if request.method == "OPTIONS":
        return jsonify({"message": "Préflight CORS réussi"}), 200

    try:
        data = request.get_json()
        recognized_text = data.get("text")
        print(f"✅ Texte reçu : {recognized_text}")

        # Traitement du texte pour obtenir la réponse météo en utilisant les coordonnées de session
        meteo = meteo_response(recognized_text, session.latitude, session.longitude)
        
        # Nettoyer chaque section des données météo en convertissant en DataFrame puis en dictionnaire JSON-compatible
        cleaned_meteo = []
        for section in meteo:
            if isinstance(section, dict):
                df = pd.DataFrame.from_dict(section)
                cleaned_section = clean_dataframe(df)
                cleaned_meteo.append(cleaned_section)
            else:
                cleaned_meteo.append(section)
                
        return jsonify({"message": "Texte reçu avec succès", "received_text": cleaned_meteo}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Erreur lors de la réception du texte", "error": str(e)}), 500

def clean_dataframe(df):
    """
    Nettoie un DataFrame en remplaçant les valeurs NaN par None et en convertissant les dates en chaînes de caractères.
    
    Paramètres:
        df (pandas.DataFrame): Le DataFrame à nettoyer.
    
    Retour:
        dict: Un dictionnaire JSON-compatible issu du DataFrame nettoyé.
    """
    if df is None or df.empty:
        return {}  # Retourne un dictionnaire vide si le DataFrame est vide

    # Remplacer les valeurs NaN par None pour assurer la compatibilité JSON
    df = df.replace({np.nan: None})

    # Convertir la colonne 'date' en chaîne de caractères, si présente
    if "date" in df.columns:
        df["date"] = df["date"].astype(str)

    return df.to_dict(orient="list")

if __name__ == "__main__":
    # Démarre l'application Flask en mode debug sur toutes les interfaces réseau, port 5000.
    app.run(debug=True, host="0.0.0.0", port=5000)
