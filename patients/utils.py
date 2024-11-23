# utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_welcome_email(patient):
    subject = 'Welcome to HopitalPlus!'
    message = f"Hello {patient.user.prenom} {patient.user.nom},\n\nThank you for registering at HospitalPlus! We are excited to have you with us.\n\nBest regards,\nThe HospitalPlus Team"
    from_email = settings.DEFAULT_FROM_EMAIL  # Utilise l'adresse e-mail par défaut configurée dans settings.py
    recipient_list = [patient.user.email]

    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print(f"E-mail envoyé à {patient.user.email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")
