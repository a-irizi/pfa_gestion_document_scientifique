from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField

from . import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.Utilisateur
        fields = ('email', 'prenom', 'deuxiemeNom', 'nom', 'dateNaissance')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = models.Utilisateur
        fields = ('email', 'prenom', 'deuxiemeNom', 'nom', 'dateNaissance')
