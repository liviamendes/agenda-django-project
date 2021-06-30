from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')

    def __str__(self):
        return self.name
