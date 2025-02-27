from modules.text_localisations import find_loc_in_text, geopy_lati_longi
from modules.dates_and_time_recodnition import dates_and_time_recodnition
from modules.open_meteo import get_weather 

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_city_from_coords(latitude, longitude):
        geolocator = Nominatim(user_agent="meteo_app")  # Nom d'agent personnalisé obligatoire
        try:
            location = geolocator.reverse((latitude, longitude), exactly_one=True, language="fr")
            if location and "address" in location.raw:
                address = location.raw["address"]
                city = address.get("city") or address.get("town") or address.get("village") or address.get("hamlet")
                return city if city else "Ville inconnue"
            return "Aucune ville trouvée"
        except GeocoderTimedOut:
            return "Erreur de connexion au service de géolocalisation"
        


        

def meteo_response(message, latitude2, longitude2):

    # Réccupération du message grace a la commande vocal dans une variable
    message = message
    print(message)

    #Dans le message reccupération des dates
    date_time = dates_and_time_recodnition(message)
    print(date_time)                            


    #Dans le message reccupération de la ville et uniquement la première trouvée
    try:
        ville = find_loc_in_text(message)[0]
        print(ville)
        #réccupération de la latitude et longitude 
        latitude, longitude = geopy_lati_longi(ville)
        
    except IndexError :
        print('Aucune ville trouvé, Utilisation de la localisation')
        latitude, longitude = latitude2, longitude2
        ville = get_city_from_coords(latitude, longitude)
        print("Ville détectée :", ville)
    except NameError :
        print('Aucune ville trouvé, Utilisation de la localisation')
        latitude, longitude = latitude2, longitude2
        ville = get_city_from_coords(latitude, longitude)
        print("Ville détectée :", ville)

    print(latitude)
    print(longitude)



    

    

    

    




    try:
        #réccupération des données météo
        current_dict, hourly_dict, daily_dict = get_weather(latitude, longitude)
        print('resultat: \n')
        
        return [current_dict, hourly_dict, daily_dict, ville]
    except IndexError:
        print('Aucune ville trouvé et la loc n\'est meme pas activé')


