<template>
    <section class="daily-meteo">
        <p class="title">Prévisions sur 5 jours</p>
        <div class="previsions">
            <div class="prevision" v-for="(prevision, index) in limitedPrevisions" :key="index">
                <p class="jour">{{ formatDay(prevision.date) }}</p>
                <img v-bind:src="getWeatherIcon(prevision.weatherCode)" alt="icone météo">
                <p class="temperatures">{{ prevision.tempMin }}° - {{ prevision.tempMax }}°</p>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    props: {
        dailyMeteo: Object // 🔥 Reçoit les prévisions journalières
    },
    computed: {
        limitedPrevisions() {
            if (!this.dailyMeteo || !this.dailyMeteo.temperature_max || this.dailyMeteo.temperature_max.length === 0) {
                return []; // 🔥 Retourne un tableau vide si aucune donnée
            }

            return this.dailyMeteo.temperature_max.slice(0, 5).map((tempMax, index) => ({
                date: this.dailyMeteo.date?.[index] || "N/A",
                tempMax:Math.round(   tempMax)  , // 🔥 Garde 1 décimale
                tempMin:Math.round(       this.dailyMeteo.temperature_min?.[index]) ?? "--",
                weatherCode: this.dailyMeteo.weather_code?.[index] || 3 // 🔥 Valeur par défaut : "Nuageux"
            }));
        }
    },
    methods: {
        formatDay(dateString) {
            console.log("🔍 dateString reçu :", dateString);
            if (!dateString) return "--";
            const date = new Date(dateString);
            return date.toLocaleDateString("fr-FR", { weekday: "short" }); // 🔥 Affiche "Lun.", "Mar.", etc.
        },
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