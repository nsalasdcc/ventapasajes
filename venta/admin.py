from django.contrib import admin
from venta.models import Recorrido, Pasaje

# Register your models here.


class RecorridoAdmin(admin.ModelAdmin):
    readonly_fields = ('max_capacidad',)

    fieldsets = [
        ('Recorrido',  {'fields': ['origen', 'destino']}),
        ('Horarios',   {'fields': ['hora_inicio', 'hora_llegada']}),
        ('Asignar/Cambiar Bus Asignado', {'fields': ['bus_asignado', 'max_capacidad']})
    ]

    list_display = ('origen', 'destino', 'hora_inicio')

    def save_model(self, request, obj, form, change):
        obj.pasajes_vendidos = 0

        for p in range(obj.max_capacidad):
            pasaje = Pasaje(id_pasaje=None, asiento=None, vendido=False, recorrido=obj)
            pasaje.save()

        if change and obj.bus_asignado is None:
            pasajes = Pasaje.objects.filter(recorrido=obj)
            pasajes.delete()

        obj.save()

admin.site.register(Recorrido, RecorridoAdmin)

