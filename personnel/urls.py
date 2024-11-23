from django.urls import path
from . import views

urlpatterns = [
    path('', views.PersonnelListView.as_view(), name='personnel_list'),
    path('personnel/create/', views.PersonnelCreateView.as_view(), name='personnel_create'),
    path('personnel/<int:pk>/', views.PersonnelDetailView.as_view(), name='personnel_detail'),
    path('personnel/<int:pk>/update/', views.PersonnelUpdateView.as_view(), name='personnel_update'),
    path('personnel/<int:pk>/delete/', views.PersonnelDeleteView.as_view(), name='personnel_delete'),
]
