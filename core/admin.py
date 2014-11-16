from django.contrib import admin

# Register your models here.
from core.models import ArmyRequest

admin.autodiscover()
admin.site.register(ArmyRequest)
