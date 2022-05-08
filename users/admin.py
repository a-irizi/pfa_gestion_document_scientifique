from django.forms import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from . import forms
from . import models

class CustomUserAdmin(ModelAdmin):
    # The forms to add and change user instances
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm
    model = models.Utilisateur

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'nom', 'prenom', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        ('Identification', {'fields': ('email', 'password')}),
        ('Information Personelles', {'fields': ('nom', 'prenom', 'deuxiemeNom', 'dateNaissance',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('email',)
    filter_horizontal = ()

# Register your models here.
admin.site.register(models.Utilisateur, CustomUserAdmin)
admin.site.register(models.Thesard)
admin.site.register(models.Professeur)
admin.site.register(models.DirecteurLaboratoire)
admin.site.register(models.UniversiteProfile)
admin.site.register(models.FaculteProfile)
admin.site.register(models.DepartementProfile)
admin.site.register(models.LaboratoireProfile)
admin.site.register(models.CommunicationInternational)
admin.site.register(models.ChapitreOuvrage)
admin.site.register(models.PublicationRevueInternational)
