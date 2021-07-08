
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image

# Create your models here.
class Home(models.Model):
    pass

class CustomUserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



class CustomRegisterModel(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_email_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.first_name

    def __str__(self):
        """Return string representation of our user"""
        return self.email



class ProfileModel(models.Model):
    user = models.OneToOneField(CustomRegisterModel, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_picture')

    def __str__(self):
        return f"{self.user.first_name}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
