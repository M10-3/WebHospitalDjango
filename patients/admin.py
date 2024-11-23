from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin, ImportMixin
from .models import Patient

# Créer une classe Resource pour le modèle Patient
class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient
        fields = ('num_id', 'user__prenom', 'user__nom', 'user__email', 'dob', 'numero', 'adresse', 
                  'antecedents_medicaux', 'genre', 'poids', 'taille')
        export_order = ('num_id', 'user__prenom', 'user__nom', 'user__email', 'dob', 'numero', 
                        'adresse', 'antecedents_medicaux', 'genre', 'poids', 'taille')


# Créer une classe d'administration pour Patient avec les options d'importation et d'exportation
class PatientAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    resource_class = PatientResource
    list_display = ('num_id', 'get_nom', 'get_prenom', 'get_email', 'dob', 'get_genre', 'numero', 'adresse', 'antecedents_medicaux', 'poids', 'taille', 'photo_profil')

    def get_nom(self, obj):
        return obj.user.nom
    get_nom.short_description = 'Nom'

    def get_prenom(self, obj):
        return obj.user.prenom
    get_prenom.short_description = 'Prénom'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_genre(self, obj):
        return dict(Patient.GENRE_CHOICES).get(obj.genre)
    get_genre.short_description = 'Genre'

# Enregistrer le modèle et la classe d'administration
admin.site.register(Patient, PatientAdmin)
