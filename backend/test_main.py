from modules.text_localisations import find_loc_in_text, geopy_lati_longi
from modules.dates_and_time_recodnition import dates_and_time_recodnition
from modules.open_meteo import get_weather 

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from modules.text_localisations import find_loc_in_text, geopy_lati_longi
from modules.dates_and_time_recodnition import dates_and_time_recodnition
from modules.open_meteo import get_weather 

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_city_from_coords(latitude, longitude):
    """
    Récupère la ville correspondant à des coordonnées données en utilisant Nominatim.

    Paramètres:
        latitude (float): Latitude de l'emplacement.
        longitude (float): Longitude de l'emplacement.

    Retour:
        str: Nom de la ville, ou un message indiquant l'absence de résultat ou une erreur.
    """
    # Instancier le géolocaliseur avec un user_agent personnalisé (obligatoire)
    geolocator = Nominatim(user_agent="meteo_app")
    try:
        # Rechercher l'adresse correspondant aux coordonnées fournies, en forçant le résultat en français
        location = geolocator.reverse((latitude, longitude), exactly_one=True, language="fr")
        if location and "address" in location.raw:
            address = location.raw["address"]
            # Tenter d'extraire le nom de la ville en vérifiant plusieurs clés possibles
            city = address.get("city") or address.get("town") or address.get("village") or address.get("hamlet")
            return city if city else "Ville inconnue"
        return "Aucune ville trouvée"
    except GeocoderTimedOut:
        return "Erreur de connexion au service de géolocalisation"


def meteo_response(message, latitude2, longitude2):
    """
    Traite un message vocal pour extraire une date, une ville et récupérer les données météo associées.

    Paramètres:
        message (str): Texte issu de la commande vocale.
        latitude2 (float): Latitude par défaut si aucune ville n'est détectée.
        longitude2 (float): Longitude par défaut si aucune ville n'est détectée.

    Retour:
        list: [données météo actuelles, données météo horaires, données météo journalières, nom de la ville]
    """
    # Afficher le message reçu
    print(message)

    # Extraire une date pertinente du message (utile pour les prévisions)
    date_time = dates_and_time_recodnition(message)
    print(date_time)

    try:
        # Tenter d'extraire la première localisation détectée dans le message
        ville = find_loc_in_text(message)[0]
        print(ville)
        # Récupérer les coordonnées de la ville extraite
        latitude, longitude = geopy_lati_longi(ville)
    except (IndexError, NameError):
        # En cas d'absence de ville dans le message, utiliser les coordonnées par défaut
        print("Aucune ville trouvée dans le message, utilisation de la localisation par défaut")
        latitude, longitude = latitude2, longitude2
        # Déterminer le nom de la ville à partir des coordonnées par défaut
        ville = get_city_from_coords(latitude, longitude)
        print("Ville détectée :", ville)

    # Afficher les coordonnées utilisées
    print("Latitude :", latitude)
    print("Longitude :", longitude)

    try:
        # Récupérer les données météo pour les coordonnées obtenues
        current_dict, hourly_dict, daily_dict = get_weather(latitude, longitude)
        print("Résultat de la récupération météo :")
        return [current_dict, hourly_dict, daily_dict, ville]
    except IndexError:
        print("Erreur : Aucune ville trouvée et la localisation n'est pas activée")
