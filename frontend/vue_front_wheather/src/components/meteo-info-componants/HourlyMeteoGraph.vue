<template>
  <section class="graphique">
    <!-- Canvas qui accueillera le graphique Chart.js -->
    <canvas ref="hourlyChart"></canvas>
  </section>
</template>

<script>
import { Chart, registerables } from "chart.js";
// Enregistrement de tous les composants nécessaires de Chart.js
Chart.register(...registerables);

export default {
  // Le composant reçoit les données météo horaires via la prop "hourlyMeteo"
  props: {
    hourlyMeteo: Object,
  },
  mounted() {
    // Création du graphique dès que le composant est monté
    this.createChart();
  },
  watch: {
    // Surveillance des modifications dans "hourlyMeteo" pour mettre à jour le graphique
    hourlyMeteo: {
      handler() {
        this.createChart();
      },
      deep: true, // Permet de détecter les modifications à l'intérieur des objets imbriqués
    },
  },
  methods: {
    /**
     * Crée et affiche le graphique des températures horaires à l'aide de Chart.js.
     * Si les données nécessaires ne sont pas disponibles, un avertissement est affiché.
     */
    createChart() {
      // Vérification de la présence des données nécessaires
      if (!this.hourlyMeteo || !this.hourlyMeteo.temperature || !this.hourlyMeteo.date) {
        console.warn("⛔ Données horaires manquantes");
        return;
      }
  
      // Obtention du contexte 2D du canvas
      const ctx = this.$refs.hourlyChart.getContext("2d");
  
      // Suppression de l'ancien graphique s'il existe déjà
      if (this.chart) {
        this.chart.destroy();
      }
  
      // Transformation des dates en heures (format ex: "13h", "14h", etc.)
      const labels = this.hourlyMeteo.date.map((dateStr) => {
        const date = new Date(dateStr);
        return date.getHours() + "h";
      });
  
      // Récupération des températures arrondies à une décimale
      const temperatures = this.hourlyMeteo.temperature.map(temp => temp.toFixed(1));
  
      // Création d'un gradient de couleur pour le remplissage du graphique
      const gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, "#00c6ff");  // Bleu clair en haut
      gradient.addColorStop(0.5, "#7a00ff"); // Violet au milieu
      gradient.addColorStop(1, "#ff7300");    // Orange en bas
  
      // Création du graphique en ligne avec Chart.js
      this.chart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels, // Axe des X : heures
          datasets: [
            {
              label: "Température (°C)",
              data: temperatures, // Axe des Y : températures
              borderColor: "#ffffff", // Couleur de la ligne (blanc)
              backgroundColor: gradient, // Gradient pour le remplissage sous la ligne
              borderWidth: 3,
              pointRadius: 0, // Aucun point individuel sur la ligne
              pointBackgroundColor: "#ffffff", // Couleur des points si affichés
              pointBorderWidth: 2,
              pointBorderColor: "#007bff", // Couleur de bordure des points
              tension: 0.4, // Courbe lissée (plus de tension = courbe plus douce)
              fill: true, // Remplissage sous la ligne activé
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false, // Permet d'adapter le graphique à la taille du container
          scales: {
            x: {
              grid: { display: false }, // Masque la grille pour l'axe X
              ticks: { color: "#ffffff" }, // Couleur des étiquettes sur l'axe X
            },
            y: {
              grid: { color: "rgba(255,255,255,0.2)" }, // Couleur de la grille pour l'axe Y
              ticks: { color: "#ffffff" }, // Couleur des étiquettes sur l'axe Y
              beginAtZero: false, // L'axe Y ne commence pas obligatoirement à 0
            },
          },
          plugins: {
            legend: { display: false }, // Masque la légende du graphique
            tooltip: {
              backgroundColor: "#2c3e50", // Couleur de fond des info-bulles
              titleColor: "#ffffff",      // Couleur du titre dans l'info-bulle
              bodyColor: "#ffffff",       // Couleur du corps de l'info-bulle
              titleFont: { weight: "bold" },
              cornerRadius: 6,            // Arrondi des coins des info-bulles
            },
          },
        },
      });
    },
  },
};
</script>

  
  <style scoped>
  section.graphique {
    margin: 25px;
    margin-left: 0;
    margin-top: 0;
    background: linear-gradient(to bottom, #142850, #27496d);
    width: 480px;
    height: 330px;
    padding: 25px;
    padding-bottom: 15px;
    border-radius: 3px;
    font-size: 15px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  }
  canvas {
    width: 100%;
    height: 100%;
  }
  </style>
  