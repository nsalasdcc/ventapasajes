from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from venta.models import Recorrido, Pasaje


def index(request):
    return render(request, "venta/index.html")


def detalle(request, id_recorrido):
    recorrido = get_object_or_404(Recorrido, id_recorrido=id_recorrido)
    pasajes = recorrido.pasaje_set.all()

    context = {
        'recorrido': recorrido,
        'asientos': pasajes,
    }

    return render(request, "venta/detalle.html", context)


def buscar(request):
    origen = request.GET.get("origen", "")
    destino = request.GET.get("destino", "")

    lista_recorridos = Recorrido.objects.filter(origen__nombre__contains=origen).\
        filter(destino__nombre__contains=destino)

    ctx = {'lista_recorridos': lista_recorridos}

    return render(request, "venta/buscar.html", ctx)


def confirmar(request, id_recorrido, id_asiento):
    recorrido = Recorrido.objects.get(id_recorrido=id_recorrido)
    asiento = Pasaje.objects.get(id=id_asiento)

    if asiento.recorrido_id != recorrido.id_recorrido:
        raise ValidationError('Invalid value: %s' % id_asiento)

    ctx = {
        'recorrido': recorrido,
        'asiento': asiento,
    }
    return render(request, "venta/confirmar.html", ctx)


def vender(request, id_pasaje):
    try:
        pasaje = Pasaje.objects.get(id=id_pasaje)
        if pasaje.vendido:
            raise IntegrityError('Pasaje ya vendido')
        pasaje.vendido = True

        pasaje.save()

        success_msg = "Pasaje vendido Exitosamente."

        #TODO: introducir mensaje de exito
        redirect = HttpResponseRedirect(reverse('detalle', args=(pasaje.recorrido.id_recorrido,)))
        return redirect

    except IntegrityError:
        #TODO: Vista incorrecta!
        return render(request, "venta/confirmar.html")