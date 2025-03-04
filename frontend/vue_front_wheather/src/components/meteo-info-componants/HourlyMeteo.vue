<template>
    <section class="hourly-meteo">
      <p class="title">Prévisions horaires</p>
      <!-- Boucle sur les prévisions limitées pour afficher l'heure, l'icône et la température -->
      <div class="previsions">
        <div class="prevision" v-for="(prevision, index) in limitedPrevisions" :key="index">
          <!-- Affichage de l'heure formatée -->
          <p class="heure">{{ formatHour(prevision.date) }}</p>
          <!-- Affichage de l'icône météo correspondante -->
          <img v-bind:src="getWeatherIcon(prevision.weatherCode)" alt="icone météo">
          <!-- Affichage de la température arrondie -->
          <p class="temperatures">{{ prevision.temperature }}°</p>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    // Reçoit les données météo horaires via la prop "hourlyMeteo"
    props: {
      hourlyMeteo: Object
    },
    computed: {
      /**
       * Limite les prévisions affichées en sélectionnant un sous-ensemble
       * de l'array de températures (indices 2 à 7) et en associant à chaque
       * prévision la date, la température arrondie et le code météo.
       */
      limitedPrevisions() {
        if (!this.hourlyMeteo || !this.hourlyMeteo.temperature || this.hourlyMeteo.temperature.length === 0) {
          return []; // Retourne un tableau vide si aucune donnée n'est disponible
        }
  
        // On utilise slice(2, 8) pour sélectionner un intervalle spécifique d'heures
        return this.hourlyMeteo.temperature.slice(2, 8).map((temp, index) => ({
          // Récupère la date correspondante ou "N/A" si indisponible
          date: this.hourlyMeteo.date[index] || "N/A",
          // Arrondi la température et garde 1 décimale si besoin
          temperature: Math.round(temp),
          // Récupère le code météo ou définit "3" par défaut (Nuageux)
          weatherCode: this.hourlyMeteo.weather_code[index] || 3
        }));
      }
    },
    methods: {
      /**
       * Formate une chaîne de date pour afficher uniquement l'heure.
       * Décale l'heure de 1 pour ajuster, et gère le dépassement de 24 heures.
       *
       * @param {String} dateString - La date en chaîne de caractères.
       * @returns {String} L'heure formatée suivie de "h".
       */
      formatHour(dateString) {
        if (!dateString) {
          return "--";
        }
        // Conversion en objet Date pour récupérer l'heure
        let hour = new Date(dateString).getHours();
        // Décalage d'une heure (ajustement spécifique)
        hour += 1;
        // Gestion du dépassement de 24 heures
        if (hour >= 24) {
          hour -= 24;
        }
        return hour + "h";
      },
  
      /**
       * Retourne l'URL de l'icône météo correspondante au code météo fourni.
       *
       * @param {Number} weatherCode - Le code météo à interpréter.
       * @returns {String} L'URL de l'image associée.
       */
      getWeatherIcon(weatherCode) {
        const iconMap = {
          0: new URL('../../assets/images/sun.png', import.meta.url).href,
          1: new URL('../../assets/images/sun_cloud.png', import.meta.url).href,
          2: new URL('../../assets/images/partly_cloudy.png', import.meta.url).href,
          3: new URL('../../assets/images/cloud.png', import.meta.url).href,
          51: new URL('../../assets/images/light_rain.png', import.meta.url).href,
          53: new URL('../../assets/images/moderate_rain.png', import.meta.url).href,
          61: new URL('../../assets/images/shower_rain.png', import.meta.url).href,
          63: new URL('../../assets/images/heavy_rain.png', import.meta.url).href,
          80: new URL('../../assets/images/thunderstorm.png', import.meta.url).href,
          81: new URL('../../assets/images/heavy_thunderstorm.png', import.meta.url).href
        };
        // Retourne l'image correspondante ou une image par défaut si le code n'est pas reconnu
        return iconMap[weatherCode] || new URL('../../assets/images/cloud_example.png', import.meta.url).href;
      }
    }
  };
  </script>
  
<style scoped>
section.hourly-meteo{
    margin: 25px;
    margin-left: 0;
    margin-top: 0;
    background-image: linear-gradient(to bottom,#c9e5ffb9,#a5edffb5);
    width: 480px;
    height: 190px;
    padding: 25px;
    padding-bottom: 15px;
    border-radius: 3px;
    font-size: 15px;
    margin-bottom: 50px;
}

section.hourly-meteo p.title {
    margin-bottom:10px;
}

div.previsions{
    display: flex;
    width: 100%;
    justify-content: space-between;
    position: relative;
    right: -10px;
}
div.prevision{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

div.prevision p.jour{
    font-weight: 700;
}


div.prevision img{
    width: 40px;
    height: 30px;
    position: relative;
    left: -10px;
}

div.prevision p.temperatures{
    text-align: center;
    position: relative;
    left: -13px;
    margin-bottom: 0;
}

p.heure, p.temperatures{
    font-weight: 600;
}


</style>