from django.db import models
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.core import validators


class Credit(models.Model):
    CURRENCYS = (
        ('BTC', 'BTC'),
        ('ETH', 'ETH'),
        ('LTC', 'LTC'),
        ('DASH', 'DASH'),
    )
    LAIN_CURRENCY = (
        ('USD', 'USD'),
        ('RUR', 'RUB'),

    )
    LAIN_FORMAT = (
        ('Y', 'Y'),
        ('M', 'M'),
        ('D', 'D'),
    )

    deposit = models.CharField(max_length=30, choices=CURRENCYS)
    summary_depos = models.IntegerField()
    lain = models.CharField(max_length=30, choices=LAIN_CURRENCY)
    max_lain = models.IntegerField()
    format_lain = models.CharField(max_length=30, choices=LAIN_FORMAT)
    time_lain = models.IntegerField()
    approve = models.NullBooleanField()
    date_credit = models.DateField(auto_now_add=True)
    fo_key = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE
                               )

    def __str__(self):
        user = ExtUser.objects.get(pk=self.fo_key.pk)
        return user.email


class VerificationInformation(models.Model):
    email = models.EmailField(
        blank=False,
        help_text="user@mail.ru"
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    birth_date = models.DateField(blank=False)
    adress = models.CharField(max_length=100, blank=False)
    pasport = models.ImageField(upload_to='pasports/', blank=False)
    note_bank = models.ImageField(upload_to='note_banks/', blank=False)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ExtUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            return ValueError("Email must have")

        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields
                          )
        user.set_password(password)
        user.save()
        if not ExtUser.objects.filter(email=email).exists():
            ExtUser.objects.create(user.email, user.password)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class ExtUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=35, unique=True,
                              validators=[
                                  validators.EmailValidator()
                              ])

    ver_inform_upload = models.BooleanField(default=False)
    ver_inform_approve = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ExtUserManager()

    def __str__(self):
        return self.email

    class Meta:
        permissions = (
            ("take_credit", "Can take credit"),
        )
