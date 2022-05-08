import abc
import uuid
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UtilisateurManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, nom, prenom,email, dateNaissance, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, nom=nom, prenom=prenom, dateNaissance=dateNaissance, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,nom, prenom,email, dateNaissance, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(nom, prenom,email, dateNaissance, password, **extra_fields)

    def create_superuser(self,nom, prenom,email, dateNaissance, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(nom, prenom,email, dateNaissance, password, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=200, unique=True, null=False, blank=False)
    nom = models.CharField(max_length=50, null=False, blank=False)
    deuxiemeNom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=False, blank=False)
    dateNaissance = models.DateField(null=False, blank=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False, primary_key=True)

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

class Universite(models.Model):
    nom = models.CharField(max_length=200, unique=True, null=False, blank=False)
    nomAcronym = models.CharField(max_length=200)
    id = models.UUIDField(uuid.uuid4, editable=False, unique=True, primary_key=True)

class Faculte(models.Model):
    nom = models.CharField(max_length=200, unique=True, null=False, blank=False)
    nomAcronym = models.CharField(max_length=200)
    id = models.UUIDField(uuid.uuid4, editable=False, unique=True, primary_key=True)
    universite = models.ForeignKey(to=Universite, on_delete=models.SET_NULL, null=True, blank=False)

class Departement(models.Model):
    nom = models.CharField(max_length=200, unique=True, null=False, blank=False)
    nomAcronym = models.CharField(max_length=200)
    id = models.UUIDField(uuid.uuid4, editable=False, unique=True, primary_key=True)
    faculte = models.ForeignKey(to=Faculte, on_delete=models.SET_NULL, null=True, blank=False)

class Laboratoire(models.Model):
    nom = models.CharField(max_length=200, unique=True, null=False, blank=False)
    nomAcronym = models.CharField(max_length=200)
    id = models.UUIDField(uuid.uuid4, editable=False, unique=True, primary_key=True)
    Departement = models.ForeignKey(to=Departement, on_delete=models.SET_NULL, null=True, blank=False)

class Papier(abc.ABCMeta):
    INDEX = (
        ('SCOPUS', 'Scopus'),
        ('WEB_OF_SCIENCE', 'Web Of Science'),
        ('AUTRE', 'Autre'),
        ('AUCUNE', 'Aucune'),
    )
    titre = models.CharField(max_length=200, null=False, blank=False)
    auteurs = models.ManyToManyField(to="Chercheur", null=False, blank=False)
    index = models.CharField(choices=INDEX, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(uuid.uuid4, editable=False, unique=True, primary_key=True)

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
        ('WORKSHOP', 'Workshop'),
        ('CONFERENCE', 'Conference'),
        ('AUTRE', 'Autre')
    )
    nomConference = models.CharField(max_length=300, null=False, blank=False)
    ville = models.CharField(max_length=300, null=False, blank=False)
    pays = models.CharField(max_length=300, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    pageDebut = models.IntegerField(null=False, blank=False, validators=[])
    pageFin = models.IntegerField(null=False, blank=False, validators=[])
    type = models.CharField(choices=COMMUNICATION_INTERNATIONAL_TYPE, null=False, blank=False)
