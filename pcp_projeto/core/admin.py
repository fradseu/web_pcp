from django import forms
from django.contrib import admin

# Register your models here.


from .models import Sector
from .models import Priority
from .models import Sector
from .models import Statusos
from .models import Factory


admin.site.register(Sector)
admin.site.register(Priority)
admin.site.register(Statusos)
admin.site.register(Factory)