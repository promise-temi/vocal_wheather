<template>
    <section class="daily-meteo">
      <!-- Titre de la section -->
      <p class="title">Prévisions sur 5 jours</p>
      <div class="previsions">
        <!-- Itération sur les prévisions limitées (5 jours) -->
        <div class="prevision" v-for="(prevision, index) in limitedPrevisions" :key="index">
          <!-- Affichage du jour (format abrégé : Lun., Mar., etc.) -->
          <p class="jour">{{ formatDay(prevision.date) }}</p>
          <!-- Affichage de l'icône météo correspondant au code météo -->
          <img v-bind:src="getWeatherIcon(prevision.weatherCode)" alt="icone météo">
          <!-- Affichage de la plage de températures (min et max) -->
          <p class="temperatures">{{ prevision.tempMin }}° - {{ prevision.tempMax }}°</p>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    // Le composant reçoit via prop les prévisions journalières dans l'objet "dailyMeteo"
    props: {
      dailyMeteo: Object
    },
    computed: {
      /**
       * Crée un sous-ensemble des prévisions journalières pour afficher uniquement 5 jours.
       * Pour chaque jour, il récupère la date, les températures max et min et le code météo.
       * Si les données ne sont pas disponibles, des valeurs par défaut sont utilisées.
       */
      limitedPrevisions() {
        if (
          !this.dailyMeteo ||
          !this.dailyMeteo.temperature_max ||
          this.dailyMeteo.temperature_max.length === 0
        ) {
          return []; // Retourne un tableau vide si aucune donnée n'est disponible
        }
  
        // Sélectionne les 5 premiers jours et associe les données correspondantes.
        return this.dailyMeteo.temperature_max.slice(0, 5).map((tempMax, index) => ({
          // Récupération de la date correspondante ou "N/A" en cas d'absence
          date: this.dailyMeteo.date?.[index] || "N/A",
          // Température maximale arrondie
          tempMax: Math.round(tempMax),
          // Température minimale arrondie, ou "--" si non disponible
          tempMin: Math.round(this.dailyMeteo.temperature_min?.[index]) ?? "--",
          // Code météo, avec valeur par défaut 3 (indiquant "Nuageux") si non défini
          weatherCode: this.dailyMeteo.weather_code?.[index] || 3
        }));
      }
    },
    methods: {
      /**
       * Formate une date pour afficher le jour de la semaine en format abrégé.
       * @param {String} dateString - La date en chaîne de caractères.
       * @returns {String} Jour abrégé (ex. "Lun.", "Mar.", etc.) ou "--" si la date n'est pas disponible.
       */
      formatDay(dateString) {
        console.log(" dateString reçu :", dateString);
        if (!dateString) return "--";
        const date = new Date(dateString);
        // Utilise toLocaleDateString pour obtenir le jour de la semaine en français
        return date.toLocaleDateString("fr-FR", { weekday: "short" });
      },
  
      /**
       * Retourne l'URL de l'icône météo correspondante au code météo fourni.
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
          53: new URL('../../assets/images/light_rain.png', import.meta.url).href,
          61: new URL('../../assets/images/heavy_rain.png', import.meta.url).href,
          63: new URL('../../assets/images/heavy_rain.png', import.meta.url).href,
          80: new URL('../../assets/images/thunderstorm.png', import.meta.url).href,
          81: new URL('../../assets/images/heavy_thunderstorm.png', import.meta.url).href
        };
        // Retourne l'icône correspondant ou une icône par défaut si le code n'est pas reconnu
        return iconMap[weatherCode] || new URL('../../assets/images/cloud_example.png', import.meta.url).href;
      }
    }
  };
  </script>
  
<style scoped>
section.daily-meteo{
    margin: 25px;
    margin-top: 0;
    background-image: linear-gradient(to bottom,#c9e5ffb9,#a5edffb5);
    width: 250px;
    padding: 25px;
    padding-bottom: 15px;
    border-radius: 3px;
    font-size: 15px;
}

section.daily-meteo p.title {
    margin-bottom: 0px;
}


div.prevision{
    display: flex;
    justify-content: space-between;
    margin-bottom: 0px;
    border-color: rgba(255, 255, 255, 0.518);
    border-width: 1px;
    border-bottom-style: solid;
    padding-top: 12px;
}

div.prevision p.jour{
    font-weight: 700;
}

div.prevision img{
    width: 40px;
    height:30px;
}

div.previsions div.prevision:last-child{
    border-bottom-style: none;
}
</style>