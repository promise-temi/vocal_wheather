<template>
    <section class="section-meteo-info">
      <!-- Affichage du nom de la ville et de la date actuelle -->
      <div class="ville-et-date">
        <h2>
          <!-- Icône de localisation -->
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
            <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
          </svg>
          {{ ville }}
        </h2>
        <!-- Affichage de la date actuelle au format défini -->
        <h3>{{ date }}</h3>
        
        <!-- Section contenant les différentes informations météo -->
        <div class="infos">
          <!-- Partie 1 : informations météo demandées et prévisions journalières -->
          <div class="m-partie1">
            <RequestedMeteo :currentMeteo="currentMeteo" />
            <DailyMeteo :dailyMeteo="dailyMeteo" />
          </div>
          <!-- Partie 2 : prévisions horaires et graphique associé -->
          <div class="m-partie2">
            <HourlyMeteo :hourlyMeteo="hourlyMeteo" />
            <HourlyMeteoGraph :hourlyMeteo="hourlyMeteo" />
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import RequestedMeteo from './meteo-info-componants/RequestedMeteo.vue';
  import DailyMeteo from './meteo-info-componants/DailyMeteo.vue';
  import HourlyMeteo from './meteo-info-componants/HourlyMeteo.vue';
  import HourlyMeteoGraph from './meteo-info-componants/HourlyMeteoGraph.vue';
  
  export default {
    // Définition des props reçues par le composant depuis le parent
    props: {
      currentMeteo: Object,
      dailyMeteo: Object,
      hourlyMeteo: Object,
      ville: String,
    },
    data() {
      return {
        // Génère la date actuelle formatée en français avec le jour, le jour numérique, le mois abrégé et l'heure
        date: new Date().toLocaleString("fr-FR", {
          weekday: "long",
          day: "numeric",
          month: "short",
          hour: "2-digit",
          minute: "2-digit"
        })
      };
    },
    // Déclaration des composants enfants utilisés dans le template
    components: {
      RequestedMeteo,
      DailyMeteo,
      HourlyMeteo,
      HourlyMeteoGraph,
    }
  };
  </script>
  

<style scoped>
section.section-meteo-info{
    width: 900px;
    height: 755px;
    background-color: #171717a3;
    margin: 50px;
    padding: 20px;
    margin-top: 20px;
    
}

h2{
    font-size: 20px;

}

svg{
    margin-right: 10px;
}

h3{
    font-weight: 100;
    font-size: 13px;
    position: relative;
    right: -30px;
    color: rgb(182, 182, 182);
}

div.m-partie1{
    display: flex;
    flex-direction: column;
}

div.infos{
    display: flex;
    justify-content: space-between;
}
</style>



