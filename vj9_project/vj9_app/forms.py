from django.forms import ModelForm
from .models import Korisnik, Predmeti
from django.contrib.auth.forms import UserCreationForm



class MyUserForm(UserCreationForm):
  class Meta:
    model = Korisnik
    fields = ['username', 'first_name', 'last_name', 'email', 'role', 'status', 'password1', 'password2']



class PredmetiForm(ModelForm):
  class Meta:
    model = Predmeti
    fields = ['name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'izborni']