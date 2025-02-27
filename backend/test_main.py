from modules.text_localisations import find_loc_in_text, geopy_lati_longi
from modules.dates_and_time_recodnition import dates_and_time_recodnition
from modules.open_meteo import get_weather 



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
    except NameError :
        print('Aucune ville trouvé, Utilisation de la localisation')
        latitude, longitude = latitude2, longitude2

    print(latitude)
    print(longitude)


    try:
        #réccupération des données météo
        current_dict, hourly_dict, daily_dict = get_weather(latitude, longitude)
        print('resultat: \n')
        
        return [current_dict, hourly_dict, daily_dict]
    except IndexError:
        print('Aucune ville trouvé et la loc n\'est meme pas activé')


