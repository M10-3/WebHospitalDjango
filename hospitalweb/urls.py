from django.contrib import admin
from django.urls import path, include
from personnel import views as pv
urlpatterns = [
    path('admin/', admin.site.urls),
    path('personnel/',include('personnel.urls')),
    path('patients/', include('patients.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('home/', pv.home, name='home'),
    path('',pv.main, name='main'),
]
