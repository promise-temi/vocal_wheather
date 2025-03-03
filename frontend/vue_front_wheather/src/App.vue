<template>

      <Header/>
      <Microphone @meteo-updated="updateMeteoData" />
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
      currentMeteo: null,
      hourlyMeteo: null,
      dailyMeteo: null,
      ville: null,
      latitude: null,
      longitude: null,
    }
  },
  methods: {
    updateMeteoData(meteo) {
      this.currentMeteo = meteo.currentMeteo
      this.hourlyMeteo = meteo.hourlyMeteo
      this.dailyMeteo = meteo.dailyMeteo
      this.ville = meteo.ville
    },

    getLocalisation() {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords
            this.latitude = latitude
            this.longitude = longitude

            console.log('Latitude:', this.latitude)
            console.log('Longitude:', this.longitude)

            // On peut envoyer la localisation ici
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

    async sendLocalisation() {
      // Bien déclarer la variable data
      const data = {
        longitude: this.longitude,
        latitude: this.latitude,
      }
      try {
        let result = await axios.post('http://127.0.0.1:5000/localisation', data)
        console.log(result.data)
      } catch (e) {
        console.error(e)
        console.log("une erreur s'est produite")
      }
    }
  },

  mounted() {
    // Juste getLocalisation ici
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
