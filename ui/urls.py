from django.conf.urls import patterns, url
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

urlpatterns = patterns('ui.views',
   url('^$', ensure_csrf_cookie(TemplateView.as_view(template_name='ui/index.html')), name='index'),
)
