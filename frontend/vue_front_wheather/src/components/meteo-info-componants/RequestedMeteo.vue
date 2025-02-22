<template>
    <section class="requested-meteo">
        <div class="meteo">
            <div class="temperature-et-weather-code">
                <p class="temperature">{{ temperature }}°</p>
                <p class="weather-code">{{ weatherCode }}</p>
            </div>
            <img v-bind:src="meteoIcon" alt="icone météo">
        </div>
        <div class="humidity">
            <p>{{ humidityCode }}</p>
            <div class="progress">
                <div class="progress-bar" role="progressbar" v-bind:style="{width: humidity + '%'}" v-bind="humidity" aria-valuemin="0" aria-valuemax="100">{{humidity}}%</div>
            </div>
        </div>
    </section>

</template>

<script>

export default{
    data(){
        return{
            temperature: '19',
            weatherCode: 'Mid Rain',
            meteoIcon: new URL('../../assets/images/Cloud_example.png', import.meta.url).href,
            humidityCode: "Humidité assez élevée",
            humidity: 75,

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
  },

}
</script>

<style scoped>
section.requested-meteo{
    border: solid 1px rgba(0, 0, 0, 0.148);
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