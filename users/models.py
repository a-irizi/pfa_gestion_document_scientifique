import uuid
from wsgiref.validate import validator
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from . import validators

# Create your models here.
class UtilisateurManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self, nom, prenom, email, dateNaissance, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("The given email must be set")
        email = BaseUserManager.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            dateNaissance=dateNaissance,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, nom, prenom, email, dateNaissance, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            nom, prenom, email, dateNaissance, password, **extra_fields
        )

    def create_superuser(
        self, nom, prenom, email, dateNaissance, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            nom, prenom, email, dateNaissance, password, **extra_fields
        )


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=200, unique=True, null=False, blank=False)
    nom = models.CharField(max_length=50, null=False, blank=False)
    deuxiemeNom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=False, blank=False)
    dateNaissance = models.DateField(null=False, blank=False, validators=[validators.minAgeValidator])
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, null=False, primary_key=True
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # Don't add email to REQUIRED_FIELDS, it is automatically included
    # as USERNAME_FIELD
    REQUIRED_FIELDS = ["nom", "prenom", "dateNaissance"]
    objects = UtilisateurManager()

    def __str__(self):
        result = None
        if self.deuxiemeNom:
            result = f"{self.prenom} {self.deuxiemeNom} {self.nom}"
        else:
            result = f"{self.prenom} {self.nom}"

        return result


class Chercheur(Utilisateur):
    laboratoire = models.ForeignKey(
        to="LaboratoireProfile", null=True, blank=False, on_delete=models.SET_NULL
    )


class Professeur(Chercheur):
    def validerCompteThesard(t: "Thesard"):
        t.is_active = True

    def validerPublicationThesard(t: "Thesard", p: "Papier"):
        pass

    def __str__(self):
        return "Pr. " + Chercheur.__str__(self)


class Thesard(Chercheur):
    anneeDebutDoctorat = models.IntegerField(
        null=False,
        blank=False,
        validators=[
            validators.minAnneeDebutDoctoratValidator,
            validators.maxAnneeDebutDoctoratValidator,
        ],
    )
    sujetThese = models.CharField(max_length=300, null=False, blank=False)
    directeurThese = models.ForeignKey(
        to=Professeur, null=True, blank=False, on_delete=models.SET_NULL
    )


class DirecteurLaboratoire(Professeur):
    def validerCompteProfesseur(p: Professeur):
        p.is_active = True


class Etablissement(models.Model):
    nom = models.CharField(max_length=200, unique=True, null=False, blank=False)
    nomAcronym = models.CharField(max_length=200, blank=True, null=True)
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )

    def __str__(self):
        result = None
        if self.nomAcronym:
            result = f"{self.nom} ({self.nomAcronym})"
        else:
            result = f"{self.nom}"
        return result


class UniversiteProfile(Etablissement):
    pass


class FaculteProfile(Etablissement):
    universite = models.ForeignKey(
        to=UniversiteProfile, on_delete=models.SET_NULL, null=True, blank=False
    )


class DepartementProfile(Etablissement):
    faculte = models.ForeignKey(
        to=FaculteProfile, on_delete=models.SET_NULL, null=True, blank=False
    )


class LaboratoireProfile(Etablissement):
    Departement = models.ForeignKey(
        to=DepartementProfile, on_delete=models.SET_NULL, null=True, blank=False
    )


class Papier(models.Model):
    INDEX = (
        ("SCOPUS", "Scopus"),
        ("WEB_OF_SCIENCE", "Web Of Science"),
        ("AUTRE", "Autre"),
        ("AUCUNE", "Aucune"),
    )
    titre = models.CharField(max_length=200, null=False, blank=False)
    auteurs = models.ManyToManyField(to="Chercheur", blank=False)
    index = models.CharField(max_length=50, choices=INDEX, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )


# TODO: Add Validators for annee, pageDebut, pageFin
class PublicationRevueInternational(Papier):
    journalNom = models.CharField(max_length=200, null=False, blank=False)
    journalNumero = models.IntegerField(null=False, blank=False)
    journalVolume = models.IntegerField(null=False, blank=False)
    annee = models.IntegerField(null=False, blank=False, validators=[])
    pageDebut = models.IntegerField(null=False, blank=False, validators=[])
    pageFin = models.IntegerField(null=False, blank=False, validators=[])


# TODO: Add Validators for chapitreNumero, pageDebut, pageFin
class ChapitreOuvrage(Papier):
    ouvrageNom = models.CharField(max_length=300, null=False, blank=False)
    ouvrageEdition = models.IntegerField(null=False, blank=False)
    chapitreNom = models.CharField(max_length=300, null=False, blank=False)
    chapitreNumero = models.IntegerField(null=False, blank=False)
    pageDebut = models.IntegerField(null=False, blank=False, validators=[])
    pageFin = models.IntegerField(null=False, blank=False, validators=[])


# TODO: Add Validators for date, pageDebut, pageFin
class CommunicationInternational(Papier):
    COMMUNICATION_INTERNATIONAL_TYPE = (
        ("WORKSHOP", "Workshop"),
        ("CONFERENCE", "Conference"),
        ("AUTRE", "Autre"),
    )
    nomConference = models.CharField(max_length=300, null=False, blank=False)
    ville = models.CharField(max_length=300, null=False, blank=False)
    pays = models.CharField(max_length=300, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    pageDebut = models.IntegerField(null=False, blank=False, validators=[])
    pageFin = models.IntegerField(null=False, blank=False, validators=[])
    type = models.CharField(
        max_length=200,
        choices=COMMUNICATION_INTERNATIONAL_TYPE,
        null=False,
        blank=False,
    )
