from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/', include('core.urls')),
                       url(r'^assist/', include('ui.urls')),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
                       )
