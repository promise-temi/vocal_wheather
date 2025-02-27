<template>
    <section class="hourly-meteo">
        <p class="title">Prévisions horaires</p>
        <div class="previsions">
            <div class="prevision" v-for="(prevision, index) in limitedPrevisions" :key="index">
                <p class="heure">{{ formatHour(prevision.date) }}</p>
                <img v-bind:src="getWeatherIcon(prevision.weatherCode)" alt="icone météo">
                <p class="temperatures">{{ prevision.temperature }}°</p>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    props: {
        hourlyMeteo: Object // 🔥 Reçoit les prévisions horaires
    },
    computed: {
        limitedPrevisions() {
            if (!this.hourlyMeteo || !this.hourlyMeteo.temperature || this.hourlyMeteo.temperature.length === 0) {
                return []; // 🔥 Retourne un tableau vide si aucune donnée
            }

            return this.hourlyMeteo.temperature.slice(0, 6).map((temp, index) => ({
                date: this.hourlyMeteo.date[index] || "N/A",
                temperature: temp.toFixed(1), // 🔥 Garde 1 décimale
                weatherCode: this.hourlyMeteo.weather_code[index] || 3 // 🔥 Valeur par défaut : "Nuageux"
            }));
        }
    },
    methods: {
        formatHour(dateString) {
            return dateString ? new Date(dateString).getHours() + "h" : "--";
        },
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
            return iconMap[weatherCode] || new URL('../../assets/images/default.png', import.meta.url).href;
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
    height: 175px;
    padding: 25px;
    padding-bottom: 15px;
    border-radius: 10px;
    font-size: 15px;
    
}

section.hourly-meteo p.title {
    margin-bottom: 0px;
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
    
}

div.prevision p.jour{
    font-weight: 700;
}


div.prevision img{
    width: 50px;
    position: relative;
    left: -15px;
}

div.prevision p.temperatures{
    text-align: center;
    position: relative;
    left: -13px;
    margin-bottom: 0;
}


</style>