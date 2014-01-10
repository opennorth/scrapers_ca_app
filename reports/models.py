# coding: utf-8
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

  @property
  def exception_header(self):
    return self.exception.strip().split('\n')[-1]

  @property
  def exception_teaser(self):
    return self.exception_header[:49] + (self.exception_header[49:] and u'…')

  def __unicode__(self):
    return self.module
