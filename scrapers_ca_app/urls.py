from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    ('', include('imago.urls')),
    url(r'^report/(?P<module_name>[a-z0-9_]+)/$', 'reports.views.report', name='report'),
    url(r'^represent/(?P<module_name>[a-z0-9_]+)/$', 'reports.views.represent', name='represent'),
    url(r'^warnings/$', 'reports.views.warnings', name='warnings'),
    url(r'^$', 'reports.views.home', name='home'),
)
