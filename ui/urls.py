from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('ui.views',
   url('^$', TemplateView.as_view(template_name='ui/index.html'), name='index'),
   url('^distance/$', TemplateView.as_view(template_name='ui/distance.html'), name='index'),
)
