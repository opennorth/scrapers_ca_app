from django.db import models

# Create your models here.
class Report(models.Model):
  name = models.TextField()
  status = models.TextField()
  error = models.TextField()
