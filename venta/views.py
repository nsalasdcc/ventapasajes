from django.shortcuts import render, get_object_or_404
from venta.models import Recorrido


def index(request):
    return render(request, "venta/index.html")


def detalle(request, id_recorrido):
    recorrido = get_object_or_404(Recorrido, id_recorrido=id_recorrido)

    context = {
        'recorrido': recorrido
    }

    return render(request, "venta/detalle.html", context)


def buscar(request):
    origen = request.GET.get("origen", "")
    destino = request.GET.get("destino", "")

    lista_recorridos = Recorrido.objects.filter(origen__nombre__contains=origen).\
        filter(destino__nombre__contains=destino)

    ctx = {'lista_recorridos': lista_recorridos}

    return render(request, "venta/buscar.html", ctx)