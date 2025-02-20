from modules.speech_recognition import recognize_from_microphone
from modules.text_localisations import find_loc_in_text, geopy_lati_longi
from modules.dates_and_time_recodnition import dates_and_time_recodnition
from modules.open_meteo import get_weather


def main():

    #Réccupération du message grace a la commande vocal dans une variable
    message = recognize_from_microphone()
    print(message)

    #Dans le message reccupération des dates
    date_time = dates_and_time_recodnition(message)
    print(date_time)

    #Dans le message reccupération de la ville et uniquement la première trouvée
    try:
        ville = find_loc_in_text(message)[0]
        print(ville)
    except IndexError :
        print('Aucune ville trouvé, Veuillez recommance ou activer votre localisation')

    #réccupération de la latitude et longitude 
    latitude, longitude = geopy_lati_longi(ville)
    print(latitude)
    print(longitude)

    #réccupération des données météo
    current_dict, hourly_dict, daily_dict = get_weather(latitude, longitude)
        
    

  



if __name__ == "__main__":
    main()