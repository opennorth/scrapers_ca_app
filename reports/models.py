from django.db import models
from django_hstore import hstore

class Report(models.Model):
  id = models.AutoField(primary_key=True)
  module = models.CharField(max_length=100)
  report = hstore.DictionaryField(null=True)
  exception = models.TextField()
  updated_at = models.DateTimeField(auto_now=True)
  success_at = models.DateTimeField(null=True)
  objects = hstore.HStoreManager()

  def __unicode__(self):
    return self.module
