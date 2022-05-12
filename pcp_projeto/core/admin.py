from django import forms
from django.contrib import admin

# Register your models here.


from .models import Sector,Priority,Statusos,Factory,Type_service,Procedimento,Solicitacao,Ferr_report




admin.site.register(Sector)
admin.site.register(Priority)
admin.site.register(Statusos)
admin.site.register(Factory)
admin.site.register(Type_service)
admin.site.register(Procedimento)
admin.site.register(Solicitacao)
admin.site.register(Ferr_report)