from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient
from .forms import PatientForm
from .forms import PatientRegistrationForm, PatientUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from .utils import send_welcome_email
from django.http import JsonResponse
from django.shortcuts import render
from .predictions import train_model_with_cross_validation
import csv
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from sklearn.metrics import roc_curve, auc

def home_patient(request):
    patient = None  # Assurez-vous que 'patient' est défini au début
    if 'patient_id' in request.session:
        try:
            patient = Patient.objects.get(id=request.session['patient_id'])
            print(f"Patient found: {patient.user.nom} {patient.user.prenom}")  # Debugging output
        except Patient.DoesNotExist:
            print("No patient found with that ID")
    
    return render(request, 'home.html', {'patient': patient})


#l'ajout d'un patient
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_patient')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

#afficher les patients
def list_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'list_patient.html', {'patient': patient})

#Modifier les patients 
def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, request.FILES, instance=patient)  # Utiliser le formulaire de mise à jour
        if form.is_valid():
            # Récupérer l'option sélectionnée pour le dossier médical
            dossier_medical_option = form.cleaned_data.get('dossier_medical_option')

            if dossier_medical_option == 'import':
                # Logique pour gérer l'importation du dossier médical
                # Ici, vous pourriez lire le contenu du fichier PDF et le stocker ou simplement mettre à jour le champ
                patient.antecedents_medicaux = "Dossier médical importé."  # Placeholder pour le texte
            elif dossier_medical_option == 'input':
                patient.antecedents_medicaux = form.cleaned_data.get('dossier_medical_text')
            else:
                patient.antecedents_medicaux = None  # Aucun dossier médical

            # Sauvegarder le patient
            form.save()
            return redirect('list_patient', patient_id=patient.id)
    else:
        initial_data = {
            'email': patient.user.email,
            'nom': patient.user.nom,
            'prenom': patient.user.prenom,
        }
        form = PatientUpdateForm(instance=patient, initial=initial_data)  # Instance existante pour pré-remplir le formulaire

    return render(request, 'update_patient.html', {'form': form, 'patient': patient})

#supprimer les patients 
def delete_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('login')
    return render(request, 'delete_patient.html', {'patient': patient})


# Inscription d'un patient
def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()  # Enregistre le patient et l'utilisateur associé
            send_welcome_email(patient)  # Appel de la fonction pour envoyer l'e-mail
            messages.success(request, 'Student registration successful! A welcome email has been sent.')
            messages.success(request, "Vous vous êtes inscrit avec succès!")
            return redirect('login')
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


# Connexion d'un patient 
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Utilisation de la méthode authenticate pour vérifier les identifiants
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)  # Connexion de l'utilisateur
            request.session['patient_id'] = user.patient.id  # Si vous souhaitez stocker le patient dans la session
            return redirect('home_patient')
        else:
            messages.error(request, "Identifiants invalides!")
    return render(request, 'login.html')


# Connexion d'un patient 

def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')  # Redirige vers la page de connexion

#*********************************************IA********************************

def model_results_view(request):
    if request.method == 'POST':
        # Entraîner le modèle et obtenir les métriques et prédictions
        model, mean_accuracy, f1, roc_auc, X_test, y_test, y_pred_proba = train_model_with_cross_validation()

        # Chargement des données des patients
        patients = Patient.objects.all()
        data = [{'age': 2024 - p.dob.year, 'imc': p.poids / ((p.taille / 100) ** 2)} for p in patients if p.taille and p.poids]
        df = pd.DataFrame(data)

        # Récupérer les données du patient connecté
        connected_patient = Patient.objects.filter(user=request.user).first()
        patient_message = ""
        patient_recommendation = ""
        if connected_patient and connected_patient.taille and connected_patient.poids:
            # Calculer les caractéristiques du patient connecté
            patient_data = {
                'age': 2024 - connected_patient.dob.year,
                'genre': {'M': 0, 'F': 1, 'O': 2}.get(connected_patient.genre, 2),
                'poids': connected_patient.poids,
                'taille': connected_patient.taille,
                'imc': connected_patient.poids / ((connected_patient.taille / 100) ** 2),
            }
            # Convertir en DataFrame pour prédiction
            patient_df = pd.DataFrame([patient_data])
            prob_readmission = model.predict_proba(patient_df)[0][1]  # Probabilité de réadmission
            patient_message = f"Votre probabilité de réadmission est de {prob_readmission:.2%}."

            # Ajouter des recommandations
            if prob_readmission <= 0.30:
                patient_recommendation = "Votre risque de réadmission est faible. Continuez à suivre vos soins habituels."
            elif prob_readmission <= 0.60:
                patient_recommendation = "Votre risque de réadmission est modéré. Pensez à planifier une visite de contrôle."
            else:
                patient_recommendation = "Votre risque de réadmission est élevé. Veuillez consulter un médecin dès que possible."
        else:
            patient_message = "Impossible de calculer votre risque de réadmission : données insuffisantes."

        # Génération de l'histogramme des âges
        plt.figure(figsize=(6, 4))
        plt.hist(df['age'], bins=10, color='skyblue', edgecolor='black')
        plt.title('Répartition des âges')
        plt.xlabel('Âge')
        plt.ylabel('Nombre de patients')
        buffer_age = BytesIO()
        plt.savefig(buffer_age, format='png')
        buffer_age.seek(0)
        graphic_age = base64.b64encode(buffer_age.getvalue()).decode('utf-8')
        buffer_age.close()

        # Génération de la courbe ROC
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc_value = auc(fpr, tpr)

        plt.figure(figsize=(6, 4))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_value:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.title('Receiver Operating Characteristic')
        plt.xlabel('Taux de faux positifs')
        plt.ylabel('Taux de vrais positifs')
        plt.legend(loc='lower right')
        buffer_roc = BytesIO()
        plt.savefig(buffer_roc, format='png')
        buffer_roc.seek(0)
        graphic_roc = base64.b64encode(buffer_roc.getvalue()).decode('utf-8')
        buffer_roc.close()

        # Ajout des graphiques et des métriques au contexte
        context = {
            'mean_accuracy': round(mean_accuracy * 100, 2),
            'f1_score': round(f1, 2),
            'roc_auc': round(roc_auc, 2),
            'message': "Le modèle a été entraîné avec succès !",
            'graphic_age': graphic_age,
            'graphic_roc': graphic_roc,
            'patient_message': patient_message,  # Message personnalisé
            'patient_recommendation': patient_recommendation,  # Recommandation personnalisée
        }
    else:
        # Afficher une page de démarrage
        context = {
            'message': "Cliquez sur le bouton pour entraîner le modèle.",
        }

    return render(request, 'model_results.html', context)



def download_report(request):
    # Préparer une réponse HTTP pour un fichier CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)

    # Ajouter un en-tête au fichier CSV
    writer.writerow(['Numero ID', 'Nom', 'Prenom', 'Age', 'Genre', 'IMC', 'Performance'])

    # Récupérer les patients pour inclure dans le rapport
    patients = Patient.objects.all()

    # Ajoute les performances du modèle si pertinent
    try:
        model, mean_accuracy, f1, roc_auc = train_model_with_cross_validation()
        writer.writerow([])
        writer.writerow(['Performance du modele'])
        writer.writerow(['Precision moyenne (%)', round(mean_accuracy * 100, 2)])
        writer.writerow(['F1 Score', round(f1, 2)])
        writer.writerow(['ROC-AUC Score', round(roc_auc, 2)])
        writer.writerow([])
    except Exception as e:
        writer.writerow([])
        writer.writerow(['Erreur lors de lentraînement du modele'])
        writer.writerow([str(e)])
        writer.writerow([])

    # Ajouter les détails des patients
    for patient in patients:
        genre = dict(Patient.GENRE_CHOICES).get(patient.genre, "N/A")
        imc = patient.imc if patient.imc else "N/A"
        writer.writerow([
            patient.num_id,
            patient.user.nom,
            patient.user.prenom,
            patient.age,
            genre,
            imc,
            'Donnees incluses'
        ])

    return response
