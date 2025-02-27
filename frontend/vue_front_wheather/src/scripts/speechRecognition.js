import * as sdk from "microsoft-cognitiveservices-speech-sdk";

const SPEECH_KEY = import.meta.env.VITE_SPEECH_KEY;
const SPEECH_REGION = import.meta.env.VITE_SPEECH_REGION;

export function recognizeFromMicrophone() {
    return new Promise((resolve, reject) => {
        try {
            const speechConfig = sdk.SpeechConfig.fromSubscription(SPEECH_KEY, SPEECH_REGION);
            speechConfig.speechRecognitionLanguage = "fr-FR";

            const audioConfig = sdk.AudioConfig.fromDefaultMicrophoneInput();
            const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

            console.log("🎤 Parlez maintenant...");

            recognizer.recognizeOnceAsync(
                (result) => {
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
                (err) => {
                    console.error("Erreur :", err);
                    reject(err);
                }
            );
        } catch (error) {
            console.error("Erreur :", error);
            reject(error);
        }
    });
}
