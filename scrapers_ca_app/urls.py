from django.urls import path, re_path

from reports import views

urlpatterns = [
    re_path(r'^report/(?P<module_name>[a-z0-9_]+)/$', views.report, name='report'),
    re_path(r'^represent/(?P<module_name>[a-z0-9_]+)/$', views.represent, name='represent'),
    re_path(r'^run/(?P<module_name>[a-z0-9_]+)/$', views.run, name='run'),
    path('warnings/', views.warnings, name='warnings'),
    path('', views.home, name='home'),
]
