from django.contrib import admin
from venta.models import Recorrido, Pasaje

import hashlib


class RecorridoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Recorrido',  {'fields': ['origen', 'destino']}),
        ('Horarios',   {'fields': ['hora_inicio', 'hora_llegada']}),
        ('Bus Asignado', {'fields': ['bus_asignado']})
    ]

    list_display = ('origen', 'destino', 'hora_inicio')

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.bus_asignado:
            for i in range(obj.bus_asignado.capacidad):
                pasaje = Pasaje()
                pasaje.precio = 10000
                pasaje.asiento = i + 1
                pasaje.recorrido = obj
                pasaje.vendido = False

                pasaje.save()

                hasho = hashlib.sha256()

                hasho.update(str(pasaje.id))
                hasho.update('--')
                hasho.update(str(pasaje.recorrido_id))

                pasaje.sid = hasho.hexdigest()
                pasaje.save()
        else:
            Pasaje.objects.filter(recorrido=obj).delete()


admin.site.register(Recorrido, RecorridoAdmin)

