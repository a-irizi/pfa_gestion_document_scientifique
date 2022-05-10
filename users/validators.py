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

def age(dob: datetime.date):
    today = datetime.date.today()
    age_ = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age_

def minAgeValidator(value):
    MIN_AGE = 23
    if age(value) < MIN_AGE:
        raise forms.ValidationError("Age est inférieur à la valeur minimale")