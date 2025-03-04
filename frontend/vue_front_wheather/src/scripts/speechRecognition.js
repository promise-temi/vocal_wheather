// Importation de l'ensemble des fonctionnalités du SDK de Microsoft Cognitive Services pour la reconnaissance vocale.
import * as sdk from "microsoft-cognitiveservices-speech-sdk";

// Récupération de la clé et de la région depuis les variables d'environnement (configurées via Vite)
const SPEECH_KEY = import.meta.env.VITE_SPEECH_KEY;
const SPEECH_REGION = import.meta.env.VITE_SPEECH_REGION;

/**
 * Fonction asynchrone qui lance la reconnaissance vocale via le microphone par défaut.
 * Retourne une promesse qui se résout avec le texte reconnu ou un message d'erreur.
 */
export function recognizeFromMicrophone() {
    return new Promise((resolve, reject) => {
        try {
            // Création de la configuration de la reconnaissance vocale avec la clé d'abonnement et la région.
            const speechConfig = sdk.SpeechConfig.fromSubscription(SPEECH_KEY, SPEECH_REGION);
            // Définition de la langue de reconnaissance en français.
            speechConfig.speechRecognitionLanguage = "fr-FR";

            // Création de la configuration audio pour utiliser le microphone par défaut.
            const audioConfig = sdk.AudioConfig.fromDefaultMicrophoneInput();
            // Instanciation du SpeechRecognizer avec la configuration de la reconnaissance et l'entrée audio.
            const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

            console.log("🎤 Parlez maintenant...");

            // Lancement de la reconnaissance vocale en mode "recognizeOnceAsync".
            recognizer.recognizeOnceAsync(
                (result) => {
                    // Selon le résultat, on résout la promesse avec le texte reconnu ou un message adapté.
                    if (result.reason === sdk.ResultReason.RecognizedSpeech) {
                        console.log("✅ Reconnu :", result.text);
                        resolve(result.text);
                    } else if (result.reason === sdk.ResultReason.NoMatch) {
                        console.log("❌ Aucune voix reconnue.");
                        resolve("Aucune voix reconnue.");
                    } else if (result.reason === sdk.ResultReason.Canceled) {
                        console.log("⚠️ Reconnaissance annulée.");
                        resolve("Reconnaissance annulée.");
                    }
                },
                // Callback en cas d'erreur lors de la reconnaissance.
                (err) => {
                    console.error("Erreur :", err);
                    reject(err);
                }
            );
        } catch (error) {
            // Gestion des erreurs potentielles lors de la configuration ou l'initialisation.
            console.error("Erreur :", error);
            reject(error);
        }
    });
}
