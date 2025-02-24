<template>
<section class="daily-meteo">
    <p class="title"></p>
    <div class="previsions">
        <div class="prevision" v-for="(prevision, index) in previsions" :key="index">
                <p class="jour">{{ prevision.date }}</p>
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
                    date : 'Maint.',
                    logo : new URL('../../assets/images/Cloud_example.png', import.meta.url).href,
                    temperatures : '13°'

                },
                {
                    date : '7h',
                    logo : new URL('../../assets/images/Cloud_example.png', import.meta.url).href,
                    temperatures : '11°'

                },
                {
                    date : '8h',
                    logo : new URL('../../assets/images/Cloud_example.png', import.meta.url).href,
                    temperatures : '5°'

                },
                {
                    date : '9h',
                    logo : new URL('../../assets/images/Cloud_example.png', import.meta.url).href,
                    temperatures : '3°'

                },
                {
                    date : '10h',
                    logo : new URL('../../assets/images/Cloud_example.png', import.meta.url).href,
                    temperatures : '13°'

                },
                {
                    date : '11h',
                    logo : new URL('../../assets/images/Cloud_example.png', import.meta.url).href,
                    temperatures : '13°'

                },

            ]
        }
    }
}
</script>
<style scoped>
section.daily-meteo{
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

section.daily-meteo p.title {
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