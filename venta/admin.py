from django.contrib import admin
from venta.models import Recorrido, Pasaje


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
        else:
            Pasaje.objects.filter(recorrido=obj).delete()


admin.site.register(Recorrido, RecorridoAdmin)

