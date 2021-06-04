from django.db import models

# Create your models here.

class Credentials(models.Model):
    name = models.CharField(max_length = 16)
    password = models.CharField(max_length = 64)
