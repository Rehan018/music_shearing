from django.db import models
from django.contrib.auth.models import User

class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    ACCESS_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    access = models.CharField(max_length=10, choices=ACCESS_CHOICES)

class AllowedUser(models.Model):
    music_file = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    email = models.EmailField()
