<template>
  <!-- Inclusion de la barre de navigation en haut de la page -->
  <Header/>

  <!-- Composant Microphone pour capturer la commande vocale.
       L'événement "meteo-updated" est émis par le composant Microphone,
       et déclenche la méthode "updateMeteoData" pour mettre à jour les données météo. -->
  <Microphone @meteo-updated="updateMeteoData" />

  <!-- Composant MeteoInfo qui affiche les informations météo.
       Les props sont liées aux données stockées dans le composant parent. -->
  <MeteoInfo 
    :currentMeteo="currentMeteo" 
    :hourlyMeteo="hourlyMeteo" 
    :dailyMeteo="dailyMeteo" 
    :ville="ville"
  />
</template>

<script>
import Header from './components/BarreDeNavigation.vue'
import MeteoInfo from './components/MeteoInfo.vue'
import Microphone from './components/Microphone.vue'
import axios from 'axios'

export default {
  components: {
    Header,
    MeteoInfo,
    Microphone,
  },
  data() {
    return {
      // Données météo reçues de l'API backend ou via la commande vocale
      currentMeteo: null,
      hourlyMeteo: null,
      dailyMeteo: null,
      // Nom de la ville détectée
      ville: null,
      // Coordonnées de localisation de l'utilisateur
      latitude: null,
      longitude: null,
    }
  },
  methods: {
    /**
     * Met à jour les données météo à partir de l'événement émis par le composant Microphone.
     * @param {Object} meteo - Objet contenant currentMeteo, hourlyMeteo, dailyMeteo et ville.
     */
    updateMeteoData(meteo) {
      this.currentMeteo = meteo.currentMeteo
      this.hourlyMeteo = meteo.hourlyMeteo
      this.dailyMeteo = meteo.dailyMeteo
      this.ville = meteo.ville
    },

    /**
     * Récupère la localisation de l'utilisateur via l'API de géolocalisation du navigateur.
     * En cas de succès, les coordonnées (latitude et longitude) sont stockées dans le data
     * et la méthode sendLocalisation() est appelée pour envoyer ces informations au backend.
     */
    getLocalisation() {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords
            this.latitude = latitude
            this.longitude = longitude

            console.log('Latitude:', this.latitude)
            console.log('Longitude:', this.longitude)

            // Envoi des coordonnées au backend
            this.sendLocalisation()
          },
          (error) => {
            console.error('Erreur de géolocalisation:', error)
          }
        )
      } else {
        console.error("La géolocalisation n'est pas supportée par ce navigateur.")
      }
    },

    /**
     * Envoie la localisation (latitude et longitude) au serveur via une requête POST.
     */
    async sendLocalisation() {
      // Construction de l'objet data avec les coordonnées
      const data = {
        longitude: this.longitude,
        latitude: this.latitude,
      }
      try {
        let result = await axios.post('http://127.0.0.1:5000/localisation', data)
        console.log(result.data)
      } catch (e) {
        console.error(e)
        console.log("Une erreur s'est produite lors de l'envoi de la localisation.")
      }
    }
  },

  /**
   * Hook "mounted" : appelé lorsque le composant est monté dans le DOM.
   * Ici, il déclenche la récupération de la localisation.
   */
  mounted() {
    this.getLocalisation()
  }
}
</script>


<style scoped>
*{
  margin:0px;
  padding: 0px;
  box-sizing: border-box;
  color: white;
}






</style>
