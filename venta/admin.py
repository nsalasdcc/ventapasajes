from django.contrib import admin
from venta.models import Recorrido

# Register your models here.


class RecorridoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Recorrido',  {'fields': ['origen', 'destino']}),
        ('Horarios',   {'fields': ['hora_inicio', 'hora_llegada']}),
    ]

    list_display = ('origen', 'destino', 'hora_inicio')

admin.site.register(Recorrido, RecorridoAdmin)

