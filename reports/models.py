from django.db import models

# Create your models here.
class Report(models.Model):
  name = models.TextField()
  status = models.CharField(max_length=50)
  error = models.TextField(max_length=1000)
