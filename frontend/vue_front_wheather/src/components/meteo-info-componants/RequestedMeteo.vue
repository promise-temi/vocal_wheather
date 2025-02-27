<template>
    <section class="requested-meteo">
        <div class="meteo">
            <div class="temperature-et-weather-code">
                <p class="temperature">{{ computedTemperature }}°</p>
                <p class="weather-code">{{ computedWeatherCode }}</p>
            </div>
            <img v-bind:src="computedMeteoIcon" alt="icone météo">
        </div>
        <div class="humidity">
            <p>{{ computedHumidityCode }}</p>
            <div class="progress">
                <div class="progress-bar" role="progressbar" 
                    v-bind:style="{width: computedHumidity + '%'}" 
                    aria-valuemin="0" aria-valuemax="100">
                    {{ computedHumidity }}%
                </div>
            </div>
        </div>
    </section>
</template>

<script>

export default {
    props: {
        currentMeteo: Object
    },
    computed: {
        computedTemperature() {
    const rawTemp = this.currentMeteo?.temperature?.[0];
    if (rawTemp == null) {
      return "--";
    }
    return Math.round(rawTemp);  // ou rawTemp.toFixed(1)
  },
  computedWeatherCode() {
    return this.getWeatherDescription(this.currentMeteo?.weather_code?.[0]);
  },
        computedMeteoIcon() {
            return this.getMeteoIcon(this.currentMeteo?.weather_code?.[0]);
        },
        computedHumidity() {
            return this.currentMeteo?.humidity ?? 0;
        },
        computedHumidityCode() {
            return this.getHumidityDescription(this.currentMeteo?.humidity);
        }
    },
    methods: {
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
        getMeteoIcon(weatherCode) {
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
            return iconMap[weatherCode] ?? new URL('../../assets/images/default.png', import.meta.url).href;
        },
        getHumidityDescription(humidity) {
            if (humidity >= 80) return "Humidité élevée";
            if (humidity >= 50) return "Humidité modérée";
            return "Humidité faible";
        }
    },
    mounted() {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css";
    document.head.appendChild(link);

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
    right: -10px;
}

div.meteo img{
    
    width: 150px;
    height: 120px;
}

div.humidity{
    border: solid rgba(255, 255, 255, 0.167) 1px;
    padding : 20px 0;
    border-left: none;
    border-right: none;
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