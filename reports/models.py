from django.db import models

# Create your models here.
class Report(models.Model):
  name = models.CharField(max_length=50)
  status = models.CharField(max_length=50)
  error = models.CharField(max_length=300)
