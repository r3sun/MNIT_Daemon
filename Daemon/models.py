from django.db import models

# Create your models here.

class Pages(models.Model):
    url = models.TextField()

class PageInf(models.Model):
    path = models.TextField()
    title = models.TextField()
    subj = models.CharField(max_length = 20)
    typ = models.CharField(max_length = 20)
    pub_time = models.DateTimeField('time_published')
    mk_array = models.TextField()
    author = models.CharField(max_length = 20)
    aprnc = models.CharField(max_length = 1)
    state = models.CharField(max_length = 1)
    views = models.IntegerField(default = 0)
