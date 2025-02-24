<template>
    <section class="vocal-command" >
        <div class="microphone" @click="showStop" v-show="recordIcon" title="Utiliser commande vocale">
            <svg  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" v-bind:class="recordIcon" viewBox="0 0 16 16">
            <path d="M5 3a3 3 0 0 1 6 0v5a3 3 0 0 1-6 0z"/>
            <path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5"/>
            </svg>
        </div>

        <div class="microphone-active" @click="showRecord" v-show="stopIcon" title="Stop">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-stop-fill" viewBox="0 0 16 16">
            <path d="M5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5A1.5 1.5 0 0 1 5 3.5"/>
            </svg>
        </div>
        
        <span>{{recordMessage}}</span>
    </section>
</template>
<script>
import axios from 'axios';
export default{
    data(){
        return{
            recordIcon: true,
            stopIcon: false,
            recordMessage: 'Effectuer une recherche vocale'
        }
    },
    methods:{
        showStop(){
            this.recordIcon = false
            this.stopIcon = true
            this.recordMessage = 'C\'est à vous...'
        },
        showRecord(){
            this.recordIcon = true
            this.stopIcon = false
            this.recordMessage = 'Effectuer une recherche vocale'
        },
        
        activateRecording(){
            axios.get('')
        }

    }
}

</script>
<style scoped>
section.vocal-command{
    color: white;
    margin-left: 50px;
    display: flex;
}

div.microphone{
    background-color: #1717172c;
    width: 50px;
    height: 50px;
    display: flex;
    justify-content: center;
    border: #8a8a8aa3 1px solid;
    border-radius: 50%;
    padding-top: 15px;
}

div.microphone:hover{
    
    cursor: pointer;
}

div.microphone-active{
    background-color: red;
    width: 50px;
    height: 50px;
    display: flex;
    justify-content: center;
    border: #8a8a8aa3 1px solid;
    border-radius: 50%;
    padding-top: 12px;
}



section.vocal-command span{
    margin-top: 10px;
    margin-left: 30px;
}



</style>