import openai
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS

openai.api_key = settings.OPENAI_API_KEY

# Liste des symptômes associés à des maladies graves
SYMPTOMES_GRAVES = {
    "diabète": ["soif excessive", "urine fréquente", "fatigue extrême", "vision floue", "perte de poids inexpliquée"],
    "cancer": ["perte de poids inexpliquée", "fatigue persistante", "douleur localisée", "toux persistante", "saignements inhabituels"],
    "AVC (Accident Vasculaire Cérébral)": ["faiblesse soudaine d'un côté du corps", "difficulté à parler", "perte de vision", "maux de tête sévères"],
    "insuffisance cardiaque": ["essoufflement", "gonflement des jambes", "fatigue extrême", "difficulté à respirer en position allongée"],
    "infarctus du myocarde (crise cardiaque)": ["douleur thoracique", "difficulté à respirer", "douleur irradiant dans le bras gauche", "nausées"],
    "maladie rénale chronique": ["gonflement des chevilles", "fatigue", "perte d'appétit", "difficulté à respirer", "urine mousseuse"],
    "hépatite virale": ["jaunisse (peau et yeux jaunes)", "fatigue", "nausées", "douleur abdominale", "perte d'appétit"],
    "HIV (SIDA)": ["perte de poids importante", "fièvre persistante", "toux chronique", "infections récurrentes", "transpiration nocturne"],
    "tuberculose": ["toux persistante", "perte de poids", "sueurs nocturnes", "fièvre", "douleurs thoraciques"],
    "maladie de Parkinson": ["tremblements", "raideur musculaire", "difficulté à marcher", "troubles de l'équilibre", "difficulté à parler"],
}

# URL pour prendre un rendez-vous médical (remplace avec l'URL réelle de ton application de rendez-vous)
RAPPEL_RDV_URL = "http://localhost:8000/rendezvous/prendre-rdv/"  # Remplace par ton URL réelle

@csrf_exempt
def chatbot_response(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []  # Initialisation de l'historique si c'est la première fois

    if request.method == 'POST':
        user_message = request.POST.get('message')
        print(f"Message reçu: {user_message}")
        
        # Ajouter le message utilisateur à l'historique de la session
        request.session['chat_history'].append({"role": "user", "content": user_message})

        try:
            # Utilisation de l'API OpenAI avec l'historique complet et un ton empathique
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ou "gpt-4" si tu l'as activé
                messages=request.session['chat_history']  # Envoi de l'historique complet
            )
            # Extraction de la réponse du chatbot
            bot_message = response['choices'][0]['message']['content']
            
            # Vérifier si des symptômes graves sont mentionnés
            for maladie, symptomes in SYMPTOMES_GRAVES.items():
                for symptome in symptomes:
                    if symptome.lower() in user_message.lower():
                        # Si un symptôme grave est détecté, ajout du lien de rendez-vous
                        bot_message += (
                            f"\n\nIl semble que vos symptômes pourraient être liés à un problème de santé grave, "
                            f"comme {maladie}. Il est important de consulter un médecin pour un diagnostic précis. "
                            f"Vous pouvez prendre un rendez-vous médical ici : {RAPPEL_RDV_URL}"
                        )
                        break  # Dès qu'on détecte un symptôme grave, on sort de la boucle et ajoute le lien
            
            # Ajouter la réponse du chatbot à l'historique
            request.session['chat_history'].append({"role": "assistant", "content": bot_message})
        
        except Exception as e:
            bot_message = f"Erreur OpenAI: {str(e)}"
        
        # Sauvegarder les modifications dans la session
        request.session.modified = True
        
        return JsonResponse({'response': bot_message})





@csrf_exempt
def chatbot_audio(request):
    if request.method == 'POST' and 'audio' in request.FILES:
        # Transcrire l'audio avec Whisper
        audio_file = request.FILES['audio']
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        user_message = transcript['text']

        # Générer une réponse avec GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Tu es un assistant médical virtuel rassurant qui pose des questions "
                    "et aide à diagnostiquer les patients."
                )},
                {"role": "user", "content": user_message}
            ]
        )
        bot_message = response['choices'][0]['message']['content']

        # Générer une réponse vocale
        tts = gTTS(bot_message, lang="fr")
        tts.save("response.mp3")

        # Retourner le texte et le lien vers l'audio
        return JsonResponse({'response_text': bot_message, 'audio_url': "/media/response.mp3"})

    return JsonResponse({'error': "Aucun fichier audio reçu."})
