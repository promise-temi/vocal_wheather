<template>
    <section class="daily-meteo">
        <p class="title">Prévisions sur 5 jours</p>
        <div class="previsions">
            <div class="prevision" v-for="(prevision, index) in previsions" :key="index">
                <p class="jour">{{ prevision.date }}.</p>
                <img v-bind:src="prevision.logo" alt="">
                <p class="temperatures">{{ prevision.temperatures }}</p>
            </div>
        </div>
    </section>
</template>
<script>
export default{
    data(){
        return{
            previsions : [
                {
                    date : 'Auj',
                    logo : '*',
                    temperatures : '13° - 12°'

                },
                {
                    date : 'Lun',
                    logo : '*',
                    temperatures : '11° - 13°'

                },
                {
                    date : 'Mar',
                    logo : '*',
                    temperatures : '5° - 17°'

                },
                {
                    date : 'Mer',
                    logo : '*',
                    temperatures : '3° - 12°'

                },
                {
                    date : 'Jeu',
                    logo : '*',
                    temperatures : '13° - 14°'

                },
            ]
        }
    }
}
</script>
<style scoped>
section.daily-meteo{
    margin: 25px;
    background-image: linear-gradient(to bottom,#c9e5ffb9,#a5edffb5);
    width: 250px;
    padding: 25px;
    padding-bottom: 15px;
    border-radius: 10px;
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

div.previsions div.prevision:last-child{
    border-bottom-style: none;
}
</style>