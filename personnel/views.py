from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Personnel
from django.shortcuts import render
from patients.models import Patient

#home
"""def home(request):
    patient = None  # Assurez-vous que 'patient' est défini au début
    if 'patient_id' in request.session:
        try:
            patient = Patient.objects.get(id=request.session['patient_id'])
            print(f"Patient found: {patient.user.nom} {patient.user.prenom}")  # Debugging output
        except Patient.DoesNotExist:
            print("No patient found with that ID")
    
    return render(request, 'home.html', {'patient': patient})"""

def main(request):
    
    return render(request, 'main.html')

def home(request):
    
    return render(request, 'home.html')

# Fetch
class PersonnelListView(ListView):
    model = Personnel
    template_name = 'personnel_list.html'
    context_object_name = 'personnels'
    

# Fetch by id
class PersonnelDetailView(DetailView):
    model = Personnel
    template_name = 'personnel_detail.html'
    context_object_name = 'personnel'

# Create
class PersonnelCreateView(CreateView):
    model = Personnel
    template_name = 'personnel_form.html'
    fields = ['nom', 'prenom', 'fonction', 'telephone', 'email', 'adresse']
    success_url = reverse_lazy('personnel_list')

# update
class PersonnelUpdateView(UpdateView):
    model = Personnel
    template_name = 'personnel_form.html'
    fields = ['nom', 'prenom', 'fonction', 'telephone', 'email', 'adresse']
    success_url = reverse_lazy('personnel_list')

# Delete
class PersonnelDeleteView(DeleteView):
    model = Personnel
    template_name = 'personnel_delete.html'
    success_url = reverse_lazy('personnel_list')

