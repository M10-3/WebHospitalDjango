from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)
