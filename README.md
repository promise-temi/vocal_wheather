
---

# Vocal Weather

Ce projet **Vocal Weather** vous permet de bénéficier d'une application vocale pour consulter la météo. Ce document vous guidera à travers l'installation et le démarrage du projet.

---

## Pré-requis

- **Terminal recommandé :** Utilisez l'invite de commandes (Command Prompt) pour exécuter les commandes.
- **Éditeur de code :** Visual Studio Code.
- **Node.js :** Téléchargez et installez Node.js via [ce lien](https://nodejs.org/en/download).

---

## Étapes d'installation

### 1. Création du projet et de l'environnement virtuel

- **Créer un dossier de projet :**  
  Créez un dossier sur votre machine et ouvrez-le dans VS Code.

- **Créer l'environnement virtuel :**  
  Dans le terminal, exécutez la commande suivante à la racine du projet :
  ```bash
  python -m venv venv
  ```

### 2. Activation de l'environnement virtuel

- **Sur Windows :**
  ```bash
  venv\scripts\activate
  ```
- **Sur Linux :**
  ```bash
  source venv/bin/activate
  ```
*Une fois activé, le terminal affichera le nom de votre environnement.*

### 3. Configuration des variables d'environnement

- **Créer le fichier `.env` :**  
  À la racine du projet, créez un fichier nommé `.env`.

- **Ajouter les variables d'environnement :**
  ```
  SPEECH_KEY=votre-cle
  SPEECH_REGION=votre-region
  ```

### 4. Clonage du dépôt GitHub

- **Cloner le projet :**  
  Toujours à la racine du projet, exécutez dans Git Bash ou Command Prompt :
  ```bash
  git clone https://github.com/promise-temi/vocal_wheather.git
  ```

### 5. Installation des dépendances

- **Installer les dépendances Python :**  
  Avec l'environnement virtuel activé et à la racine, lancez :
  ```bash
  pip install -r requirements.txt
  ```

---

## Structure du Projet

Le projet se compose de deux dossiers principaux :

- **backend :** Partie serveur réalisée avec Flask.
- **frontend :** Partie client réalisée avec Vue.js.

---

## Démarrage du Projet

### 1. Lancement du serveur backend

- **Accéder au dossier backend :**
  ```bash
  cd vocal_wheather/backend
  ```

- **Démarrer le serveur :**
  ```bash
  python main.py
  ```
*Le serveur se lance et affiche un message indiquant qu'il est opérationnel.*

### 2. Lancement du frontend

- **Vérifier l'installation de Node.js :**  
  Si Node.js n'est pas installé, installez-le depuis [ce lien](https://nodejs.org/en/download).

- **Accéder au dossier frontend :**  
  Ouvrez un nouveau terminal (Command Prompt recommandé) et naviguez vers :
  ```bash
  cd vocal_wheather/frontend/vue_front_wheather
  ```

- **Installer les dépendances et démarrer l'application :**
  ```bash
  npm build
  npm run dev
  ```

- **Accéder à l'application :**  
  Une fois le serveur lancé, ouvrez votre navigateur et rendez-vous sur :
  ```
  http://localhost:5173/
  ```

---

Ces instructions détaillées vous permettront de configurer et de démarrer facilement le projet **Vocal Weather**. Bonne utilisation et amusez-vous bien !