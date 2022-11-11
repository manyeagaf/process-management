from tokenize import blank_re
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    first_name = models.CharField(
        max_length=50, verbose_name=_("first name"),
    )
    middle_name = models.CharField(
        max_length=50, verbose_name=_("middle name"), null=True, blank=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name=_("last name"),
    )
    BRANCH_CHOICES = (
        (2, "Ebankese Branch"),
        (3, "Accra Central Branch"),
        (4, "Republic Court Branch"),
        (5, "Kumasi Branch"),
        (6, "Tema Branch"),
        (7, "Legon Branch"),
        (8, "Abossey Okai Branch"),
        (9, "Tudu Branch"),
        (10, "Techiman Branch"),
        (11, "KNUST Brach"),
        (12, "Tamale Branch"),
        (13, "Koforidua Branch"),
        (14, "Baatsona Branch"),
        (15, "Private Panking"),
        (16, "Ashaiman Branch"),
        (17, "Takoradi Branch"),
        (18, "Kasoa Branch"),
        (19, "Post Office Square Branch"),
        (20, "Adabraka Branch"),
        (21, "Agona Swedru Branch"),
        (22, "Cape Coast Branch"),
        (23, "Winneba Branch"),
        (24, "Asamankese Branch"),
        (25, "Dansoman Branch"),
        (26, "Accra Newtown Branch"),
        (27, "Sefwi Wiawso"),
        (28, "Essam Branch"),
        (29, "Asankragua Branch"),
        (30, "Sefwi Bekwai Branch "),
        (31, "Akontombra Branch"),
        (32, "Juaboso"),
        (33, "Asempaneye Branch"),
        (34, "Madina Branch"),
        (35, "Goaso Branch"),
        (36, "Achimota Branch"),
        (37, "Asokwa Branch"),
        (38, "Tema Community 25 Branch"),
        (39, "Bolgatanga Branch"),
        (40, "Adjiringanor Branch"),
    )
    branch = models.PositiveBigIntegerField(choices=BRANCH_CHOICES,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_branch_user = models.BooleanField(default=False)
    is_head_office_user = models.BooleanField(default=False)
    staff_id = models.CharField(max_length=50,null=True,blank=True)
    is_delete_requested = models.BooleanField(default= False)
    USER_TYPE_CHOICES = (
        (1, 'branch'),
        (2, 'officer'),
        (3, 'admin'),
        (4,'access control admin'),
        (5,'access control staff'),
    )
    role = models.CharField(max_length=200,null=True,blank = True)
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,null=True,blank=True)
    date_started = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Privilege(models.Model):
    privilege = models.CharField(max_length=300)
    slug = models.SlugField(max_length=250,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.privilege

class UserPrivilege(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,blank = True,null=True,related_name="created_by")
    is_active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name="approved_by",null=True)
    approved_at = models.DateTimeField(null=True,blank=True)
    is_delete_requested = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Logging(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=250)

class UserType(models.Model):
    title = models.CharField(max_length= 150)
    slug = models.SlugField(max_length=200,null= True,blank = True)