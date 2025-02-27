<template>
    <section class="graphique">
       
      <canvas ref="hourlyChart"></canvas>
    </section>
  </template>
  
  <script>
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);
  
  export default {
    props: {
      hourlyMeteo: Object, // 🔥 Reçoit les données météo horaires
    },
    mounted() {
      this.createChart();
    },
    watch: {
      // 🔄 Mettre à jour le graphique si les données changent
      hourlyMeteo: {
        handler() {
          this.createChart();
        },
        deep: true,
      },
    },
    methods: {
      createChart() {
        if (!this.hourlyMeteo || !this.hourlyMeteo.temperature || !this.hourlyMeteo.date) {
          console.warn("⛔ Données horaires manquantes");
          return;
        }
  
        const ctx = this.$refs.hourlyChart.getContext("2d");
  
        // Supprimer l'ancien graphique s'il existe
        if (this.chart) {
          this.chart.destroy();
        }
  
        // Transformer les dates en heures (ex: "13h", "14h"…)
        const labels = this.hourlyMeteo.date.map((dateStr) => {
          const date = new Date(dateStr);
          return date.getHours() + "h";
        });
  
        // Températures arrondies à 1 décimale
        const temperatures = this.hourlyMeteo.temperature.map(temp => temp.toFixed(1));
  
        // 🔥 Création d'un gradient pour la couleur de remplissage
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, "#00c6ff");  // Bleu clair
        gradient.addColorStop(0.5, "#7a00ff"); // Violet
        gradient.addColorStop(1, "#ff7300");  // Orange
  
        // Création du graphique avec Chart.js
        this.chart = new Chart(ctx, {
          type: "line",
          data: {
            labels: labels, // 🕒 Heures
            datasets: [
              {
                label: "Température (°C)",
                data: temperatures, // 🌡️ Températures
                borderColor: "#ffffff", // Bordure blanche
                backgroundColor: gradient, // Gradient appliqué
                borderWidth: 3,
                pointRadius: 0,
                pointBackgroundColor: "#ffffff", // Points blancs
                pointBorderWidth: 2,
                pointBorderColor: "#007bff",
                tension: 0.4, // 💡 Courbe lissée
                fill: true, // Remplissage sous la ligne
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: "#ffffff" }, // Couleur des labels X
              },
              y: {
                grid: { color: "rgba(255,255,255,0.2)" },
                ticks: { color: "#ffffff" }, // Couleur des labels Y
                beginAtZero: false,
              },
            },
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: "#2c3e50",
                titleColor: "#ffffff",
                bodyColor: "#ffffff",
                titleFont: { weight: "bold" },
                cornerRadius: 6,
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
  