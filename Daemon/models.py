from django.db import models

# Create your models here.

class Pages(models.Model):
    url = models.TextField()

class PageInf(models.Model):
    url = models.TextField()
    path = models.TextField()
    title = models.TextField()
    subj = models.CharField(max_length = 20)
    typ = models.CharField(max_length = 20)
    pub_time = models.DateTimeField('time_published')
    last_modified = models.DateTimeField('time_last_modified')
    mk_array = models.TextField()
    author = models.CharField(max_length = 20)
    views = models.IntegerField(default = 0)

class Deltd_Pages(models.Model):
    url = models.TextField()
    path = models.TextField()
    title = models.TextField()
    subj = models.CharField(max_length = 20)
    typ = models.CharField(max_length = 20)
    pub_time = models.DateTimeField('time_published')
    last_modified = models.DateTimeField('time_last_modified')
    mk_array = models.TextField()
    author = models.CharField(max_length = 20)
    views = models.IntegerField(default = 0)

class Mdfd_Pages(models.Model):
    url = models.TextField()
    path = models.TextField()
    title = models.TextField()
    subj = models.CharField(max_length = 20)
    typ = models.CharField(max_length = 20)
    pub_time = models.DateTimeField('time_published')
    last_modified = models.DateTimeField('time_last_modified')
    mk_array = models.TextField()
    author = models.CharField(max_length = 20)
    views = models.IntegerField(default = 0)
