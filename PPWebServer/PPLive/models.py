from django.db import models

class PPConfig(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)