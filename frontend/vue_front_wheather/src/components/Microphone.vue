<template>
    <section class="vocal-command">
      <div class="microphone" @click="showStop" v-show="recordIcon" title="Utiliser commande vocale">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16" height="16"
          fill="currentColor"
          :class="recordIcon"
          viewBox="0 0 16 16"
        >
          <path d="M5 3a3 3 0 0 1 6 0v5a3 3 0 0 1-6 0z"/>
          <path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1
                   a5 5 0 0 1-4.5 4.975V15h3
                   a.5.5 0 0 1 0 1h-7
                   a.5.5 0 0 1 0-1h3v-2.025
                   A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5"/>
        </svg>
      </div>
  
      <div
        class="microphone-active"
        @click="showRecord"
        v-show="stopIcon"
        :class="{ disabled: isRecording }"
        title="Stop"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="25" height="25"
          fill="currentColor"
          class="bi bi-stop-fill"
          viewBox="0 0 16 16"
        >
          <path d="M5 3.5h6
                   A1.5 1.5 0 0 1 12.5 5v6
                   a1.5 1.5 0 0 1-1.5 1.5H5
                   A1.5 1.5 0 0 1 3.5 11V5
                   A1.5 1.5 0 0 1 5 3.5"/>
        </svg>
      </div>
  
      <span>{{ recordMessage }}</span>
    </section>
  </template>
  
  <script>
  import axios from "axios";
  import { recognizeFromMicrophone } from "../scripts/speechRecognition";
  
  export default {
    // Si tu es sur Vue 3, déclare l'événement "meteo-updated" pour éviter les avertissements
    emits: ["meteo-updated"],
  
    data() {
      return {
        recordIcon: true,
        stopIcon: false,
        recordMessage: "Effectuer une recherche vocale",
        isRecording: false,
        currentMeteo: null,
        hourlyMeteo: null,
        dailyMeteo: null
      };
    },
  
    methods: {
      showStop() {
        if (this.isRecording) return;
        this.recordIcon = false;
        this.stopIcon = true;
        this.recordMessage = "Préparez-vous...";
        this.startRecognition();
      },
  
      showRecord() {
        if (this.isRecording) return;
        this.recordIcon = true;
        this.stopIcon = false;
        this.recordMessage = "Effectuer une recherche vocale";
      },
  
      async startRecognition() {
        try {
          this.isRecording = true;
          this.recordMessage = "Écoute en cours...";
  
          const result = await recognizeFromMicrophone();
          this.recordMessage = `Texte reconnu : ${result}`;
  
          // Envoyer le texte à Flask
          this.sendTextToFlask(result);
  
        } catch (error) {
          this.recordMessage = "Erreur lors de la reconnaissance vocale.";
          console.error("Erreur :", error);
        } finally {
          this.isRecording = false;
          this.recordIcon = true;
          this.stopIcon = false;
        }
      },
  
      async sendTextToFlask(text) {
        try {
          const response = await axios.post("http://127.0.0.1:5000/save-text", { text });
          console.log("✅ Réponse de Flask :", response.data);
  
          const receivedData = response.data.received_text;
  
          if (Array.isArray(receivedData) && receivedData.length >= 3) {
            // Mise à jour des propriétés locales
            this.currentMeteo = receivedData[0];
            this.hourlyMeteo = receivedData[1];
            this.dailyMeteo = receivedData[2];
  
            // Émission de l'événement avec les données météo
            console.log("🚀 Émission de l'événement meteo-updated !");
            this.$emit("meteo-updated", {
              currentMeteo: this.currentMeteo,
              hourlyMeteo: this.hourlyMeteo,
              dailyMeteo: this.dailyMeteo
            });
          } else {
            console.error("❌ Données météo incorrectes :", receivedData);
          }
  
          this.recordMessage = `Flask : ${response.data.message}`;
  
        } catch (error) {
          console.error("❌ Erreur lors de l'envoi à Flask :", error);
          this.recordMessage = "Erreur lors de l'envoi à Flask.";
        }
      }
    }
  };
  </script>

<style scoped>
/* 🔥 Désactiver le bouton Stop quand la reconnaissance tourne */
.disabled {
    pointer-events: none;
    opacity: 0.5;
}
</style>

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