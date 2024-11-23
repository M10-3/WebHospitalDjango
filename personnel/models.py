from django.db import models

class Personnel(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.fonction}"
