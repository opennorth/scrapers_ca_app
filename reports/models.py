# coding: utf-8
from django.db import models
from jsonfield import JSONField

class Report(models.Model):
  id = models.AutoField(primary_key=True)
  module = models.CharField(max_length=100)
  report = JSONField(null=True)
  exception = models.TextField()
  updated_at = models.DateTimeField(auto_now=True)
  success_at = models.DateTimeField(null=True)

  @property
  def exception_header(self):
    return self.exception.strip().split('\n')[-1]

  def __unicode__(self):
    return self.module
