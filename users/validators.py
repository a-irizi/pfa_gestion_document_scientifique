import datetime
import django.forms.forms as forms

def currentYear():
    return datetime.date.today().year;

def minAnneeDebutDoctoratValidator(value):
    if value < (currentYear() - 6 + 1):
        raise forms.ValidationError("Année de début du doctorat est inférieure à la valeur minimale")

def maxAnneeDebutDoctoratValidator(value):
    if value > currentYear():
        raise forms.ValidationError("Année de début du doctorat est supérieure à la valeur maximale")