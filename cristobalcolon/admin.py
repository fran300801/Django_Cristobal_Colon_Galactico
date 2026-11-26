from django.contrib import admin

from .models import Caracteristica, Usuario, Nave, Mision, Exoplaneta

# Register your models here.
admin.site.register(Caracteristica)
admin.site.register(Usuario)
admin.site.register(Nave)
admin.site.register(Mision)
admin.site.register(Exoplaneta)
