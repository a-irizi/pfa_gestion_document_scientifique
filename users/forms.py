from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from . import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.Utilisateur
        fields = ('email', 'prenom', 'deuxiemeNom', 'nom', 'dateNaissance')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.Utilisateur
        fields = ('email', 'prenom', 'deuxiemeNom', 'nom', 'dateNaissance')
