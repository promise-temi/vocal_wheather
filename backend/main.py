from modules.speech_recognition import recognize_from_microphone
from modules.text_localisations import find_loc_in_text, geopy_lati_longi
from modules.dates_and_time_recodnition import dates_and_time_recodnition
from test_main import meteo_response
from modules.open_meteo import get_weather
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# 📌 Autoriser les requêtes CORS y compris celles avec credentials
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

class Session:
    def __init__(self, latitude="", longitude=""):
        latitude = latitude
        longitude = longitude

session = Session()

@app.route('/localisation', methods=['POST', 'OPTIONS'])
def localisation():
    if request.method == "OPTIONS":
        return jsonify({"message": "Préflight CORS réussi"}), 200  # Répondre correctement à l'OPTIONS
    try:
        data = request.get_json()
        print(data['longitude'])
        print(data['latitude'])
        session.latitude = data['latitude']
        session.longitude = data['longitude']

        return jsonify({'message': 'bien recu'}), 200
    except:
        return jsonify({'message': 'Une erreur s\'est produite'}), 500

@app.route('/save-text', methods=['POST', 'OPTIONS'])
def save_text():
    if request.method == "OPTIONS":
        return jsonify({"message": "Préflight CORS réussi"}), 200  # Répondre correctement à l'OPTIONS

    try:
        data = request.get_json()
        recognized_text = data.get("text")
        print(f"✅ Texte reçu : {recognized_text}")
        meteo = meteo_response(recognized_text,  session.latitude, session.longitude)
         # 🔥 Convertir chaque dictionnaire en DataFrame pour nettoyage
        cleaned_meteo = []
        for section in meteo:
            if isinstance(section, dict):  # Vérifier si c'est bien un dict avant conversion
                df = pd.DataFrame.from_dict(section)
                cleaned_section = clean_dataframe(df)  # Nettoyer
                cleaned_meteo.append(cleaned_section)
            else:
                cleaned_meteo.append(section)  # Si ce n'est pas un dict, ne pas modifier
        return jsonify({"message": "Texte reçu avec succès", "received_text": cleaned_meteo}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Erreur lors de la réception du texte", "error": str(e)}), 500



# def main():

#     #Réccupération du message grace a la commande vocal dans une variable
#     message = recognize_from_microphone()
#     print(message)

#     #Dans le message reccupération des dates
#     date_time = dates_and_time_recodnition(message)
#     print(date_time)

#     #Dans le message reccupération de la ville et uniquement la première trouvée
#     try:
#         ville = find_loc_in_text(message)[0]
#         print(ville)
#     except IndexError :
#         print('Aucune ville trouvé, Veuillez recommance ou activer votre localisation')

#     #réccupération de la latitude et longitude 
#     latitude, longitude = geopy_lati_longi(ville)
#     print(latitude)
#     print(longitude)

#     #réccupération des données météo
#     current_dict, hourly_dict, daily_dict = get_weather(latitude, longitude)
        
import pandas as pd    
import numpy as np

def clean_dataframe(df):
    """ Nettoie un DataFrame : remplace NaN, convertit les types, reformate les dates """
    if df is None or df.empty:
        return {}  # Retourne un dict vide si DataFrame est vide

    df = df.replace({np.nan: None})  # Remplace les NaN par None (JSON-friendly)

    # Convertir les dates en string si elles existent
    if "date" in df.columns:
        df["date"] = df["date"].astype(str)

    return df.to_dict(orient="list")  # Convertit en dict JSON-compatible
  



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)