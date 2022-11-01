import jwt

from datetime import datetime, timedelta
from goldapi.utils import get_ip
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

# from django.utils import timezone
from datetime import datetime, timedelta
# from .generators import generate_client_id, generate_client_secret


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def register_user(self, ip_address, username, email,password=None,confirm_password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an email address')


        user = self.model(username=username,ip_address=ip_address,email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin,TimestampedModel):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.

    MANAGER = 1
    REALTOR = 2
        
    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (REALTOR, 'Realtor'),
    )

    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(db_index=True, unique=True)

    ip_address=models.CharField(max_length=120, default='ABC')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    is_realtor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()


    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. 
        We return their username instead.
        """
        return self.username


    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

# class Application(models.Model):
#     """[Application model which stores the client id and client secret which we provide\
#         for an application to consume our Rest API.]
#     Arguments:
#         models {[model]} -- [Each model is a Python class that subclasses django.db.models.Model.]
#     Returns:
#         [model] -- [Each attribute of the model represents a database field.]
#     """
#     client_id = models.CharField(
#         max_length=100, unique=True, default=generate_client_id, db_index=True
#     )
#     client_secret = models.CharField(
#         max_length=100, unique=True, default=generate_client_id, db_index=True
#     )
#     application_name = models.CharField(max_length=255)
#     activate = models.BooleanField(default=True)
#     created_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.application_name


# class AuthToken(models.Model):
#     """[Model which stored the access token for different application that is added to our DB]
#     Arguments:
#         models {[model]} -- [Each model is a Python class that subclasses django.db.models.Model.]
#     Returns:
#         [model] -- [Each attribute of the model represents a database field.]
#     """
#     access_token = models.CharField(max_length=100, unique=True)
#     refresh_token = models.CharField(max_length=100, unique=True)
#     expiry_date = models.DateTimeField()
#     refresh_token_expiry = models.DateTimeField()
#     expired = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
#     application = models.OneToOneField(
#         Application, on_delete=models.CASCADE, related_name="app_name", primary_key=True
#     )
#     def __str__(self):
#         return self.application