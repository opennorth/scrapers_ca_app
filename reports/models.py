# coding: utf-8
from django.db import models
from jsonfield import JSONField


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.CharField(max_length=100)
    report = JSONField(null=True)
    warnings = models.TextField()
    exception = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    success_at = models.DateTimeField(null=True)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def warnings_count(self):
        return len(self.warnings.split('\n'))

    @property
    def exception_header(self):
        return self.exception.strip().split('\n')[-1]

    @property
    def aggregation(self):
        return self.module.endswith('_municipalities')

    def __unicode__(self):
        return self.module
