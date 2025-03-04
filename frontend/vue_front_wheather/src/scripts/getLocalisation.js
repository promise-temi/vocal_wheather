// Définition des options pour la géolocalisation
var options = {
  enableHighAccuracy: true, // Active l'utilisation de la meilleure précision possible (ex. GPS)
  timeout: 5000,            // Délai maximal d'attente en millisecondes (ici, 5 secondes)
  maximumAge: 0             // Indique que l'on souhaite une position fraîche (aucune position en cache)
};

// Fonction de succès appelée si la géolocalisation aboutit
function success(pos) {
  // Récupération des coordonnées depuis l'objet position retourné
  var crd = pos.coords;

  console.log("Votre position actuelle est :");
  console.log(`Latitude : ${crd.latitude}`);      // Affiche la latitude
  console.log(`Longitude : ${crd.longitude}`);    // Affiche la longitude
  console.log(`La précision est de ${crd.accuracy} mètres.`); // Affiche la précision en mètres
}

// Fonction d'erreur appelée en cas de problème lors de la géolocalisation
function error(err) {
  // Affiche un message d'erreur avec le code et le message associé
  console.warn(`ERREUR (${err.code}): ${err.message}`);
}

// Demande de la position actuelle en utilisant les options définies
// success: fonction callback pour le succès, error: fonction callback pour l'erreur
navigator.geolocation.getCurrentPosition(success, error, options);
