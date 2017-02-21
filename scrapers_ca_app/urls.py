from django.conf.urls import url, include
from reports import views

urlpatterns = [
    url(r'^report/(?P<module_name>[a-z0-9_]+)/$', views.report, name='report'),
    url(r'^represent/(?P<module_name>[a-z0-9_]+)/$', views.represent, name='represent'),
    url(r'^warnings/$', views.warnings, name='warnings'),
    url(r'^$', views.home, name='home'),
]
