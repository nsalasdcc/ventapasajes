from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from venta.models import Recorrido, Pasaje


@require_GET
def index(request):
    return render(request, "venta/index.html")


@require_GET
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


@require_GET
def confirmar(request, id_recorrido, sid_asiento):
    recorrido = Recorrido.objects.get(id_recorrido=id_recorrido)
    asiento = Pasaje.objects.get(sid=sid_asiento)

    if asiento.vendido:
        raise Http404

    ctx = {
        'recorrido': recorrido,
        'asiento': asiento,
    }
    return render(request, "venta/confirmar.html", ctx)


@require_POST
def vender(request, sid_asiento):
    try:
        pasaje = Pasaje.objects.get(sid=sid_asiento)
        if pasaje.vendido:
            raise Http404
        pasaje.vendido = True

        pasaje.save()

        success_msg = "Pasaje comprado Exitosamente."

        #TODO: introducir mensaje de exito
        redirect = HttpResponse(mimetype='application/pdf')
        redirect['Content-Disposition'] = 'attachment; filename=boleto.pdf'
        p = canvas.Canvas(redirect)
        w, h = letter
        p.drawString(100, h-50, "Buses El Pintor")
        p.drawString(100, h-80, "Detalles de su Pasaje:")
        p.drawString(100, h-110, "Origen:")
        p.drawString(100+150, h-110, str(pasaje.recorrido.origen))
        p.drawString(100, h-140, "Hora salida:")
        p.drawString(100+150, h-140, str(pasaje.recorrido.hora_inicio))
        p.drawString(100, h-170, "Destino:")
        p.drawString(100+150, h-170, str(pasaje.recorrido.destino))
        p.drawString(100, h-200, "Hora llegada:")
        p.drawString(100+150, h-200, str(pasaje.recorrido.hora_llegada))
        p.drawString(100, h-230, "Bus asignado:")
        p.drawString(100+150, h-230, str(pasaje.recorrido.bus_asignado.patente))
        p.drawString(100, h-260, "Asiento")
        p.drawString(100+150, h-260, str(pasaje.asiento))
        p.drawString(100, h-350, "Gracias por preferirnos!")
        p.drawString(100, h-370, "Disfrute su viaje!")
        p.save()
        return redirect

    except IntegrityError:
        #TODO: Vista incorrecta!
        return render(request, "venta/confirmar.html")


@require_GET
def cambiar(request):
    return render(request, "venta/cambiar.html")


@require_GET
def cambiacion(request):
    sid_pasaje = request.GET.get("sid", "")

    pasaje = get_object_or_404(Pasaje, sid=sid_pasaje)

    if not pasaje.vendido:
        raise Http404

    recorrido = pasaje.recorrido
    ctx = {
        'asiento': pasaje,
        'recorrido': recorrido
    }

    return render(request, "venta/cambiacion.html", ctx)


@require_POST
def do_cambiar(request, sid_asiento):
    pasaje = get_object_or_404(Pasaje, sid=sid_asiento)

    if not pasaje.vendido:
        raise Http404
    pasaje.vendido = False

    pasaje.save()

    messages.success(request, "Elija un nuevo pasaje para su cambio")
    redirect = HttpResponseRedirect(reverse('index'))

    return redirect


@require_GET
def devolver(request):
    return render(request, "venta/devolver.html")


@require_GET
def devolucion(request):
    sid_pasaje = request.GET.get("sid", "")

    pasaje = get_object_or_404(Pasaje, sid=sid_pasaje)

    if not pasaje.vendido:
        raise Http404

    recorrido = pasaje.recorrido
    ctx = {
        'asiento': pasaje,
        'recorrido': recorrido
    }

    return render(request, "venta/devolucion.html", ctx)


@require_POST
def do_devolver(request, sid_asiento):
    pasaje = get_object_or_404(Pasaje, sid=sid_asiento)

    if not pasaje.vendido:
        raise IntegrityError("Pasaje no se ha vendido. No se puede devolver")
    pasaje.vendido = False

    pasaje.save()

    messages.success(request, "Pasaje devuelto exitosamente")
    redirect = HttpResponseRedirect(reverse('index'))

    return redirect
