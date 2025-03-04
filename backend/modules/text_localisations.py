import spacy
from geopy.geocoders import Nominatim


def main():
    find_loc_in_text()
    geopy_lati_longi()


def find_loc_in_text(text):
    """
    Analyse le texte afin d'extraire les entités de type "LOC" (lieux) à l'aide de spaCy.

    Paramètres:
        text (str): Le texte à analyser.

    Retour:
        list: Une liste contenant les noms de lieux extraits.
    """
    # Charger le modèle de langue français de spaCy (version large pour de meilleures performances)
    nlp = spacy.load("fr_core_news_lg")
    
    # Traiter le texte pour obtenir un objet "doc" contenant les entités nommées
    doc = nlp(text)
    
    # Initialiser une liste pour stocker les lieux détectés
    locations = []
    
    # Parcourir toutes les entités détectées et récupérer celles de type "LOC"
    for ent in doc.ents:
        if ent.label_ == "LOC":
            print(f"{ent.text} -> {ent.label_}")
            locations.append(ent.text)
    
    return locations

def geopy_lati_longi(city):
    """
    Récupère la latitude et la longitude d'une ville donnée en utilisant le service de géolocalisation Nominatim.

    Paramètres:
        city (str): Le nom de la ville à géolocaliser.

    Retour:
        list: Une liste contenant la latitude et la longitude de la ville.
    """
    # Initialiser le géolocaliseur avec un user_agent personnalisé
    geolocator = Nominatim(user_agent="vocal_wheather")
    
    # Rechercher la ville et récupérer l'objet "location" associé
    location = geolocator.geocode(city)
    
    # Afficher quelques informations pour vérification
    print(location.address)
    print((location.latitude, location.longitude))
    print(location.raw)
    
    # Extraire la latitude et la longitude
    geo_latitude = location.latitude
    geo_longitude = location.longitude
    
    return [geo_latitude, geo_longitude]

if __name__ == "__main__":
    main()