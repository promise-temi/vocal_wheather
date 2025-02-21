<template>
    <section class="section-meteo-info">
        <div class="ville-et-date">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
                </svg>
                {{ ville }}
            </h2>
            <h3>{{ date }}</h3>
            <div class="infos">
                <RequestedMeteo/>
            </div>
        </div>
        
    </section>
</template>
<script>
import RequestedMeteo from './RequestedMeteo.vue'


export default{
    data(){
        return{
            ville: 'Paris, France',
            date : 'Jeudi 10 Fév,  15h15'
        }
    },
    components:{
        RequestedMeteo
    }
}
</script>

<style scoped>
section.section-meteo-info{
    width: 850px;
    height: 565px;
    background-color: #171717a3;
    margin: 50px;
    padding: 20px;
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
</style>



