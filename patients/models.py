from django.db import models
from django.conf import settings
from accounts.models import CustomUser  # Importation du modèle CustomUser depuis l'application accounts
import uuid
import random
import string
from datetime import date

class Patient(models.Model):
    GENRE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'other'),
    ]
     
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Lien avec le modèle d'utilisateur
    num_id = models.CharField(max_length=20, unique=True, editable=False)
    dob = models.DateField()
    numero = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    antecedents_medicaux = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, default='M')  
    photo_profil = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Ajout des nouveaux champs
    poids = models.FloatField(null=True, blank=True)  # Poids du patient en kg
    taille = models.FloatField(null=True, blank=True)  # Taille du patient en cm

    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    @property
    def imc(self):
        if self.poids and self.taille:
            taille_metre = self.taille / 100  # Convertir la taille en mètre
            return round(self.poids / (taille_metre ** 2), 2)  # IMC = poids / taille^2
        return None

    def save(self, *args, **kwargs):
        if not self.num_id:
            # Extraire les initiales du prénom et nom de famille
            initials = f"{self.user.prenom[0].upper()}{self.user.nom[0].upper()}"
            
            # Extraire l'année de naissance
            birth_year = self.dob.year
            
            # Générer une chaîne aléatoire alphanumérique de 5 caractères
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            
            # Créer l'ID personnalisé
            self.num_id = f"{initials}{birth_year}_{random_part}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}"  # Utilisattion des noms de l'utilisateur
