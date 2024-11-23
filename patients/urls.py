from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.home, name='home'),  # Page d'accueil
     path('accounts/', include('allauth.urls')), 
     path('home_patient/', views.home_patient, name='home_patient'),
    path('add/', views.add_patient, name='add_patient'),
    path('list/<int:patient_id>/', views.list_patient, name='list_patient'),
    path('update/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('model-results/', views.model_results_view, name='model_results'),
    path('download-report/', views.download_report, name='download_report'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
