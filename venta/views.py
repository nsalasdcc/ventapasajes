from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader, RequestContext
from venta.models import Recorrido


def index(request):
    lista_recorridos = Recorrido.objects.all()

    context = {
        'lista_recorridos': lista_recorridos
    }

    return render(request, "venta/index.html", context)


def detalle(request, id_recorrido):
    recorrido = get_object_or_404(Recorrido, id_recorrido=id_recorrido)
    capacidad = recorrido.bus_asignado.capacidad

    context = {
        'recorrido': recorrido,
        'capacidad': capacidad
    }

    return render(request, "venta/detalle.html", context)
