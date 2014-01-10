from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrapers_ca_app.views.home', name='home'),
    # url(r'^scrapers_ca_app/', include('scrapers_ca_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^represent/(?P<module_name>[a-z0-9_]+)/$', 'reports.views.represent', name='represent'),
    url(r'^$', 'reports.views.home', name='home'),
)
