<template>
  <section class="vocal-command">
    <!-- Icône du microphone affichée lorsque l'utilisateur peut initier l'enregistrement -->
    <div 
      class="microphone" 
      @click="showStop" 
      v-show="recordIcon" 
      title="Utiliser commande vocale">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16" height="16"
        fill="currentColor"
        :class="recordIcon"
        viewBox="0 0 16 16">
        <path d="M5 3a3 3 0 0 1 6 0v5a3 3 0 0 1-6 0z"/>
        <path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1
                 a5 5 0 0 1-4.5 4.975V15h3
                 a.5.5 0 0 1 0 1h-7
                 a.5.5 0 0 1 0-1h3v-2.025
                 A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5"/>
      </svg>
    </div>

    <!-- Icône "Stop" affichée pendant l'enregistrement pour permettre l'arrêt -->
    <div
      class="microphone-active"
      @click="showRecord"
      v-show="stopIcon"
      :class="{ disabled: isRecording }"
      title="Stop">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="25" height="25"
        fill="currentColor"
        class="bi bi-stop-fill"
        viewBox="0 0 16 16">
        <path d="M5 3.5h6
                 A1.5 1.5 0 0 1 12.5 5v6
                 a1.5 1.5 0 0 1-1.5 1.5H5
                 A1.5 1.5 0 0 1 3.5 11V5
                 A1.5 1.5 0 0 1 5 3.5"/>
      </svg>
    </div>

    <!-- Message d'état affiché à l'utilisateur -->
    <span>{{ recordMessage }}</span>
  </section>
</template>

<script>
import axios from "axios";
import { recognizeFromMicrophone } from "../scripts/speechRecognition";

export default {
  // Déclaration de l'événement "meteo-updated" pour informer le parent lors de la mise à jour des données météo
  emits: ["meteo-updated"],

  data() {
    return {
      // Contrôle l'affichage de l'icône microphone (pour démarrer l'enregistrement)
      recordIcon: true,
      // Contrôle l'affichage de l'icône d'arrêt (pour arrêter l'enregistrement)
      stopIcon: false,
      // Message informatif affiché à l'utilisateur
      recordMessage: "Effectuer une recherche vocale",
      // Indique si l'enregistrement est en cours
      isRecording: false,
      // Données météo reçues depuis le backend
      currentMeteo: null,
      hourlyMeteo: null,
      dailyMeteo: null,
      // Nom de la ville associée aux données météo
      ville: null
    };
  },

  methods: {
    /**
     * Méthode déclenchée lors du clic sur l'icône microphone pour commencer l'enregistrement.
     * Elle cache l'icône du microphone et affiche l'icône d'arrêt, puis démarre la reconnaissance vocale.
     */
    showStop() {
      if (this.isRecording) return;
      this.recordIcon = false;
      this.stopIcon = true;
      this.recordMessage = "Préparez-vous...";
      this.startRecognition();
    },

    /**
     * Méthode déclenchée lors du clic sur l'icône d'arrêt pour revenir à l'état d'attente.
     */
    showRecord() {
      if (this.isRecording) return;
      this.recordIcon = true;
      this.stopIcon = false;
      this.recordMessage = "Effectuer une recherche vocale";
    },

    /**
     * Démarre la reconnaissance vocale en appelant la fonction "recognizeFromMicrophone".
     * Après la reconnaissance, le texte obtenu est envoyé au backend pour traitement.
     */
    async startRecognition() {
      try {
        this.isRecording = true;
        this.recordMessage = "Écoute en cours...";

        // Lancer la reconnaissance vocale et attendre le résultat
        const result = await recognizeFromMicrophone();
        this.recordMessage = `Veuillez patienter`;

        // Envoyer le texte reconnu au backend
        this.sendTextToFlask(result);
      } catch (error) {
        this.recordMessage = "Erreur lors de la reconnaissance vocale.";
        console.error("Erreur :", error);
      } finally {
        // Réinitialiser l'état de l'enregistrement, indépendamment du résultat
        this.isRecording = false;
        this.recordIcon = true;
        this.stopIcon = false;
      }
    },

    /**
     * Envoie le texte reconnu au serveur Flask via une requête POST.
     * Si la réponse contient des données météo correctes, les met à jour et émet un événement vers le parent.
     *
     * @param {String} text - Le texte reconnu par la reconnaissance vocale.
     */
    async sendTextToFlask(text) {
      try {
        const response = await axios.post("http://127.0.0.1:5000/save-text", { text });
        console.log("✅ Réponse de Flask :", response.data);

        const receivedData = response.data.received_text;

        // Vérifie que les données reçues contiennent au moins trois sections (actuel, horaire, journalier)
        if (Array.isArray(receivedData) && receivedData.length >= 3) {
          // Mise à jour des données locales
          this.currentMeteo = receivedData[0];
          this.hourlyMeteo = receivedData[1];
          this.dailyMeteo = receivedData[2];
          this.ville = receivedData[3];

          // Émission de l'événement pour notifier le parent de la mise à jour des données météo
          console.log("🚀 Émission de l'événement meteo-updated !");
          this.$emit("meteo-updated", {
            currentMeteo: this.currentMeteo,
            hourlyMeteo: this.hourlyMeteo,
            dailyMeteo: this.dailyMeteo,
            ville: this.ville,
          });
        } else {
          console.error("❌ Données météo incorrectes :", receivedData);
        }

        // Réinitialise le message affiché après envoi
        this.recordMessage = "Effectuer une recherche vocale";
      } catch (error) {
        console.error("❌ Erreur lors de l'envoi à Flask :", error);
        this.recordMessage = "Une erreur s'est produite";
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