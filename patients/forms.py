from django import forms
from .models import Patient, CustomUser
from django.contrib.auth.hashers import make_password 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'dob', 'numero', 'adresse', 'antecedents_medicaux', 'genre', 'photo_profil', 'poids', 'taille']


class PatientRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label=_("Email"))
    nom = forms.CharField(max_length=100, required=True, label=_("LastName"))
    prenom = forms.CharField(max_length=100, required=True, label=_("FirstName"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=_("Confirm Password"))
    genre = forms.ChoiceField(choices=Patient.GENRE_CHOICES, label=_("Gender"))
    photo_profil = forms.ImageField(required=False, label=_("Profile Photo"))
    poids = forms.FloatField(required=False, label=_("Weight (kg)"))
    taille = forms.FloatField(required=False, label=_("Height (cm)"))
    dossier_medical_file = forms.FileField(required=False, label='Import a medical record (PDF)', help_text='Accepted formats: PDF.')
    dossier_medical_text = forms.CharField(required=False, widget=forms.Textarea, label='Medical record', help_text='You can directly enter your medical file here.')
    dossier_medical_option = forms.ChoiceField(
        choices=[
            ('import', 'Import a medical record'),
            ('input', 'Enter the medical file')
        ],
        label='Choose an option for the medical record'
    )

    class Meta:
        model = Patient
        fields = ['dob', 'numero', 'adresse', 'antecedents_medicaux', 'genre', 'photo_profil', 'poids', 'taille', 
              'dossier_medical_option', 'dossier_medical_file', 'dossier_medical_text']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        genre = cleaned_data.get("genre")
        dossier_medical_option = cleaned_data.get("dossier_medical_option")
        dossier_medical_file = cleaned_data.get("dossier_medical_file")
        dossier_medical_text = cleaned_data.get("dossier_medical_text")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        if genre not in dict(Patient.GENRE_CHOICES).keys():
            raise forms.ValidationError("Select a valid gender option.")
        
         # Validation du dossier médical
        if dossier_medical_option == 'import' and not dossier_medical_file:
            raise forms.ValidationError("Please upload a PDF file for the medical record.")
        
        if dossier_medical_option == 'input' and not dossier_medical_text:
            raise forms.ValidationError("Please enter the medical record information.")
    
    def clean_dossier_medical_file(self):
        file = self.cleaned_data.get('dossier_medical_file')
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError("The file must be a PDF.")
        return file

        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email    
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Valide le mot de passe selon les règles de Django
        return password
    
    def clean_poids(self):
        poids = self.cleaned_data.get('poids')
        if poids is not None and poids <= 0:
            raise ValidationError(_("Weight must be a positive value."))
        return poids

    def clean_taille(self):
        taille = self.cleaned_data.get('taille')
        if taille is not None and taille <= 0:
            raise ValidationError(_("Height must be a positive value."))
        return taille


    def save(self, commit=True):
        # Création de l'utilisateur CustomUser lié au patient
        user = CustomUser(
            email=self.cleaned_data['email'],
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            password=make_password(self.cleaned_data['password']),  # Hash du mot de passe
            is_staff=False  # S'assurer que ce n'est pas un utilisateur staff
        )
        
        if commit:
            user.save()

        # Création du patient lié à cet utilisateur
        patient = super().save(commit=False)
        patient.user = user  # Lier le patient à l'utilisateur CustomUser
        patient.poids = self.cleaned_data.get('poids')
        patient.taille = self.cleaned_data.get('taille')

        dossier_medical_option = self.cleaned_data.get('dossier_medical_option')
        print(f"Option dossier médical: {dossier_medical_option}")  # Debugging
        if dossier_medical_option == 'import':
        # Logique pour gérer l'importation du dossier médical
        # Ici, vous pourriez, par exemple, lire le contenu du fichier PDF et le stocker
            patient.antecedents_medicaux = "Dossier médical importé."  # Placeholder pour le texte
        elif dossier_medical_option == 'input':
            patient.antecedents_medicaux = self.cleaned_data.get('dossier_medical_text')
        else:
            patient.antecedents_medicaux = None  # Aucun dossier médical

        if commit:
            patient.save()

        return patient


class PatientUpdateForm(forms.ModelForm):
    email = forms.EmailField(label=_("Email"), required=True)
    nom = forms.CharField(max_length=100, required=True, label=_("LastName"))
    prenom = forms.CharField(max_length=100, required=True, label=_("FirstName"))

    poids = forms.FloatField(required=False, label=_("Weight (kg)"))
    taille = forms.FloatField(required=False, label=_("Height (cm)"))
    photo_profil = forms.ImageField(required=False, label=_("Profile Picture"))

    # Ajout des choix pour l'antécédent médical
    antecedents_option = forms.ChoiceField(
        choices=[
            ('file', _('Upload a PDF')),
            ('text', _('Enter a text')),
        ],
        label=_("Choose how to update medical record"),
        widget=forms.RadioSelect,  # Pour des boutons radio
        required=True
    )
    antecedents_file = forms.FileField(
        required=False,
        label=_("Medical record (PDF)"),
        help_text=_("Upload a medical record in PDF format.")
    )
    antecedents_text = forms.CharField(
        required=False,
        label=_("Medical record (text)"),
        widget=forms.Textarea,
        help_text=_("Write the medical record directly here.")
    )

    field_order = ['prenom', 'nom', 'email', 'dob', 'numero', 'adresse', 
                   'genre', 'photo_profil', 'antecedents_medicaux', 'poids', 'taille']
    
    class Meta:
        model = Patient
        fields = ['dob', 'numero', 'adresse', 'genre', 'photo_profil', 'antecedents_medicaux', 'poids', 'taille']

    def clean(self):
        """
        Validation personnalisée pour s'assurer qu'au moins un antécédent médical est fourni.
        """
        cleaned_data = super().clean()
        antecedents_option = cleaned_data.get("antecedents_option")
        antecedents_file = cleaned_data.get("antecedents_file")
        antecedents_text = cleaned_data.get("antecedents_text")

        # Validation : au moins une méthode doit être remplie selon l'option choisie
        if antecedents_option == 'file' and not antecedents_file:
            raise forms.ValidationError(_("Please upload a PDF for the medical record."))
        if antecedents_option == 'text' and not antecedents_text:
            raise forms.ValidationError(_("Please provide a text for the medical record."))

        return cleaned_data
        
    def save(self, commit=True):
        # Mettre à jour les informations utilisateur (CustomUser)
        patient = super().save(commit=False)
        user = patient.user  # Récupérer l'utilisateur lié au patient

        antecedents_option = self.cleaned_data.get("antecedents_option")
        if antecedents_option == 'file':
            # Utiliser le fichier PDF comme antécédent médical
            patient.antecedents_medicaux = "PDF uploaded"  # Vous pouvez ajouter une logique pour stocker
        elif antecedents_option == 'text':
            # Utiliser le texte fourni comme antécédent médical
            patient.antecedents_medicaux = self.cleaned_data.get("antecedents_text")

        # Mettre à jour les champs de CustomUser
        user.email = self.cleaned_data['email']
        user.nom = self.cleaned_data['nom']
        user.prenom = self.cleaned_data['prenom']

        if commit:
            user.save()  # Sauvegarder les modifications du modèle utilisateur
            patient.save()  # Sauvegarder les modifications du modèle patient
        
        return patient    
