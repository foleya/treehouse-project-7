from django.db import models

# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    bio = models.TextField()
    avatar = models.ImageField(upload_to="avatars")
