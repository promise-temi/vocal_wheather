import os
import azure.cognitiveservices.speech as speechsdk

def main():
    recognize_from_microphone()

def recognize_from_microphone():
    """
    Capture une entrée vocale via le microphone par défaut et la reconnaît
    en utilisant l'Azure Speech SDK.

    Nécessite les variables d'environnement "SPEECH_KEY" et "SPEECH_REGION".
    La langue de reconnaissance est définie sur le français ("fr-FR").

    Retourne le texte reconnu en cas de succès.
    """
    # Configurer la reconnaissance vocale avec la clé d'abonnement et la région récupérées depuis les variables d'environnement
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'),
        region=os.environ.get('SPEECH_REGION')
    )
    # Définir la langue de reconnaissance sur le français
    speech_config.speech_recognition_language = "fr-FR"

    # Configurer l'audio pour utiliser le microphone par défaut
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    
    # Créer un objet SpeechRecognizer avec la configuration de la reconnaissance vocale et de l'audio
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Inviter l'utilisateur à parler
    print("Speak into your microphone.")
    
    # Lancer la reconnaissance vocale de manière asynchrone et attendre le résultat
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # Vérifier le résultat de la reconnaissance
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # Si le discours est reconnu, afficher et retourner le texte reconnu
        recognized_text = speech_recognition_result.text
        print("Recognized: {}".format(recognized_text))
        return recognized_text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        # Si aucun discours n'est reconnu, afficher les détails
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        # Si la reconnaissance est annulée, récupérer et afficher les détails de l'annulation
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        # Si l'annulation est due à une erreur, afficher des détails supplémentaires
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

if __name__ == "__main__":
    main()

