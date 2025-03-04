import re
import dateparser
import datetime

def main():
    dates_and_time_recodnition()

def dates_and_time_recodnition(text):
    """
    Analyse un texte pour en extraire une seule date pertinente.
    
    La fonction :
      - Recherche et extrait les expressions temporelles (dates et heures).
      - Sélectionne la date la plus ancienne trouvée.
      - Associe l'heure la plus ancienne à cette date.
      - Si aucune date n'est détectée mais qu'une heure l'est, l'heure est associée à la date du jour.
    
    Paramètres:
        text (str): Texte contenant des expressions temporelles.
    
    Retour:
        datetime.datetime ou None: La date et l'heure fusionnées, ou None si rien n'est détecté.
    """
    # Expression régulière pour détecter différents formats de dates et d'heures.
    pattern = r"""
        \b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b |  # Dates classiques (ex: 10/02/2024, 2024-05-10)
        \b(?:\d{1,2}\s?h\s?(?:\d{2})?)\b |                           # Heures (ex: 10h, 14:30, 18h00, 19 h)
        \b(?:demain|après-demain|hier|aujourd'hui|minuit|midi)\b |       # Expressions directes
        \b(?:dans|il y a)\s\d+\s(?:jours?|semaines?|mois?|années?)\b |  # Expressions relatives (ex: dans 3 jours)
        \b(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)\b |    # Jours de la semaine
        \b(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\b  # Mois
    """
    
    # Extraction des correspondances dans le texte
    matches = re.findall(pattern, text, re.IGNORECASE | re.VERBOSE)
    # Nettoyage des résultats pour éliminer les espaces inutiles
    extracted_dates = [match.strip() for match in matches if match.strip()]
    
    if not extracted_dates:
        return None  # Aucun élément temporel détecté

    def normalize_hour(hour_text):
        """
        Normalise le format d'une heure pour s'assurer qu'il inclut les minutes.
        Par exemple, "18h" devient "18h00".
        """
        hour_text = hour_text.replace(" ", "")
        if re.match(r"^\d{1,2}h$", hour_text):
            return hour_text + "00"
        elif re.match(r"^\d{1,2}$", hour_text):
            return hour_text + "h00"
        return hour_text

    # Séparation des éléments correspondant aux heures et aux dates
    hours = [normalize_hour(d) for d in extracted_dates if re.match(r"\b\d{1,2}\s?h\s?(?:\d{2})?\b", d)]
    dates_only = [d for d in extracted_dates if d not in hours]

    # Conversion des dates en objets datetime
    parsed_dates = [
        dateparser.parse(date, settings={'PREFER_DATES_FROM': 'past', 'PREFER_DAY_OF_MONTH': 'first'})
        for date in dates_only
    ]
    parsed_dates = [d for d in parsed_dates if d is not None]  # Filtrer les valeurs non converties
    oldest_date = min(parsed_dates) if parsed_dates else None

    # Conversion des heures en objets datetime
    parsed_hours = [
        dateparser.parse(hour, settings={'PREFER_DATES_FROM': 'past'})
        for hour in hours
    ]
    parsed_hours = [h for h in parsed_hours if h is not None]
    oldest_hour = min(parsed_hours, key=lambda h: h.time()) if parsed_hours else None

    # Si seule une heure est détectée, l'associer à la date d'aujourd'hui
    if oldest_date is None and oldest_hour is not None:
        today = datetime.datetime.today()
        return datetime.datetime.combine(today.date(), oldest_hour.time())

    # Fusionner la date et l'heure les plus anciennes trouvées
    if oldest_date and oldest_hour:
        return datetime.datetime.combine(oldest_date.date(), oldest_hour.time())
    elif oldest_date:
        return oldest_date
    else:
        return None





if __name__=="__main__":
    main()