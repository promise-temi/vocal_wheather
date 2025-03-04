<template>
    <section class="requested-meteo">
      <!-- Affichage des informations météo principales -->
      <div class="meteo">
        <div class="temperature-et-weather-code">
          <!-- Affichage de la température arrondie -->
          <p class="temperature">{{ computedTemperature }}°</p>
          <!-- Affichage de la description du code météo -->
          <p class="weather-code">{{ computedWeatherCode }}</p>
        </div>
        <!-- Affichage de l'icône associée au code météo -->
        <img v-bind:src="computedMeteoIcon" alt="icone météo">
      </div>
      <!-- Section affichant l'humidité -->
      <div class="humidity">
        <!-- Description de l'humidité (faible, modérée ou élevée) -->
        <p>{{ computedHumidityCode }}</p>
        <!-- Barre de progression affichant le pourcentage d'humidité -->
        <div class="progress">
          <div class="progress-bar" role="progressbar" 
               v-bind:style="{ width: computedHumidity + '%' }" 
               aria-valuemin="0" aria-valuemax="100">
            {{ computedHumidity }}%
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    // Le composant attend un objet "currentMeteo" passé en prop depuis le composant parent.
    props: {
      currentMeteo: Object
    },
    computed: {
      /**
       * Calcule la température en arrondissant la première valeur de la propriété "temperature" de currentMeteo.
       * Retourne "--" si la température n'est pas disponible.
       */
      computedTemperature() {
        const rawTemp = this.currentMeteo?.temperature?.[0];
        if (rawTemp == null) {
          return "--";
        }
        return Math.round(rawTemp);
      },
      /**
       * Retourne une description textuelle du code météo à partir de la première valeur de "weather_code".
       */
      computedWeatherCode() {
        return this.getWeatherDescription(this.currentMeteo?.weather_code?.[0]);
      },
      /**
       * Calcule l'URL de l'icône à afficher selon le code météo fourni.
       */
      computedMeteoIcon() {
        return this.getMeteoIcon(this.currentMeteo?.weather_code?.[0]);
      },
      /**
       * Récupère la valeur d'humidité, ou 0 si aucune donnée n'est disponible.
       */
      computedHumidity() {
        return this.currentMeteo?.humidity ?? 0;
      },
      /**
       * Retourne une description de l'humidité (faible, modérée ou élevée).
       */
      computedHumidityCode() {
        return this.getHumidityDescription(this.currentMeteo?.humidity);
      }
    },
    methods: {
      /**
       * Retourne une description textuelle du code météo.
       * @param {Number} weatherCode - Le code météo à interpréter.
       * @returns {String} Description du temps.
       */
      getWeatherDescription(weatherCode) {
        const descriptions = {
          0: "Ciel dégagé",
          1: "Peu nuageux",
          2: "Partiellement nuageux",
          3: "Nuageux",
          51: "Pluie légère",
          53: "Pluie modérée",
          61: "Averse légère",
          63: "Averse modérée",
          80: "Orage",
          81: "Orage fort"
        };
        return descriptions[weatherCode] ?? "Inconnu";
      },
      /**
       * Retourne l'URL de l'icône correspondante au code météo.
       * Utilise des ressources locales stockées dans le dossier assets.
       * @param {Number} weatherCode - Le code météo.
       * @returns {String} URL de l'image.
       */
      getMeteoIcon(weatherCode) {
        const iconMap = {
          0: new URL('../../assets/images/sun.png', import.meta.url).href,
          1: new URL('../../assets/images/sun_cloud.png', import.meta.url).href,
          2: new URL('../../assets/images/partly_cloudy.png', import.meta.url).href,
          3: new URL('../../assets/images/cloud.png', import.meta.url).href,
          51: new URL('../../assets/images/light_rain.png', import.meta.url).href,
          53: new URL('../../assets/images/light_rain.png', import.meta.url).href,
          61: new URL('../../assets/images/heavy_rain.png', import.meta.url).href,
          63: new URL('../../assets/images/heavy_rain.png', import.meta.url).href,
          80: new URL('../../assets/images/thunderstorm.png', import.meta.url).href,
          81: new URL('../../assets/images/heavy_thunderstorm.png', import.meta.url).href
        };
        return iconMap[weatherCode] ?? new URL('../../assets/images/cloud_example.png', import.meta.url).href;
      },
      /**
       * Retourne une description textuelle de l'humidité en fonction de sa valeur.
       * @param {Number} humidity - Le pourcentage d'humidité.
       * @returns {String} Description de l'humidité.
       */
      getHumidityDescription(humidity) {
        if (humidity >= 80) return "Humidité élevée";
        if (humidity >= 50) return "Humidité modérée";
        return "Humidité faible";
      }
    },
    mounted() {
      // Ajout dynamique de la feuille de style Bootstrap pour la barre de progression
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css";
      document.head.appendChild(link);
  
      // Ajout dynamique du script Bootstrap pour les composants interactifs
      const script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js";
      document.body.appendChild(script);
    }
  };
  </script>
  
<style scoped>
section.requested-meteo{
    /* border: solid 1px rgba(0, 0, 0, 0.148); */
    margin: 25px;
    width: 250px;
}
p.temperature{
    font-size: 70px;
}
div.meteo{
    display: flex;
}

p.weather-code{
    font-size: 12px;
    position: relative;
    white-space: nowrap;
    right: -10px;
}

div.meteo img{
    
    width: 150px;
    height: 130px;
}

div.humidity{
    border: solid rgba(255, 255, 255, 0.167) 1px;
    padding : 20px 0;
    border-left: none;
    border-right: none;
    border-bottom: none;
}

div.humidity p{
    font-size: 15px;
    margin-bottom: 10px;
}

div.progress{
    border-radius: 15px;
}
div.humidity div.progress-bar{
    background-image: linear-gradient(to right, #A5EDFF, #05CCFF);
}

</style>