from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from json import JSONDecodeError

from django.views.decorators.csrf import csrf_exempt
from datetime import date
from .models import Usuario, Caracteristica, Mision, Nave, Exoplaneta
# Create your views here.

def usuario_a_diccionario(usuario):
    return {
        "id": usuario.id,
        "apodo": usuario.apodo,
        "habilidad_arma": usuario.habilidad_arma,
        "habilidad_conduccion": usuario.habilidad_conduccion,
        "capitan": usuario.capitan,
        "caracteristicas": list(
            usuario.caracteristicas.values_list("nombre", flat=True)
        ),
    }


def listar_usuarios(request):
    if request.method != "GET":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    usuarios = [usuario_a_diccionario(u) for u in Usuario.objects.all()]
    return JsonResponse(usuarios, safe=False)


def listar_usuario_concreto(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    usuario = Usuario.objects.filter(id=id).first()

    if usuario is None:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    return JsonResponse(usuario_a_diccionario(usuario))

@csrf_exempt
def crear_usuario(request):
    if request.method != "POST":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(datos, dict):
        return JsonResponse({"error": "Se esperaba un objeto JSON"}, status=400)

    apodo = datos.get("apodo")
    if not isinstance(apodo, str) or not apodo.strip():
        return JsonResponse({"error": "El apodo es obligatorio"}, status=400)

    habilidad_arma = datos.get("habilidad_arma", 0)
    habilidad_conduccion = datos.get("habilidad_conduccion", 0)
    for valor in (habilidad_arma, habilidad_conduccion):
        # bool es subclase de int en Python, así que lo descartamos aparte
        if not isinstance(valor, int) or isinstance(valor, bool) or not 0 <= valor <= 100:
            return JsonResponse(
                {"error": "Las habilidades deben ser enteros entre 0 y 100"},
                status=400
            )

    capitan = datos.get("capitan", False)
    if not isinstance(capitan, bool):
        return JsonResponse({"error": "El campo capitan debe ser true o false"}, status=400)

    nombres = datos.get("caracteristicas", [])
    if not isinstance(nombres, list):
        return JsonResponse({"error": "caracteristicas debe ser una lista"}, status=400)

    caracteristicas = Caracteristica.objects.filter(nombre__in=nombres)
    if caracteristicas.count() != len(set(nombres)):
        return JsonResponse({"error": "Alguna característica no existe"}, status=400)

    usuario = Usuario.objects.create(
        apodo=apodo.strip(),
        habilidad_arma=habilidad_arma,
        habilidad_conduccion=habilidad_conduccion,
        capitan=capitan
    )
    usuario.caracteristicas.set(caracteristicas)

    return JsonResponse(
        {"mensaje": "Usuario creado correctamente", "id": usuario.id},
        status=201
    )

@csrf_exempt
def actualizar_usuario(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(datos, dict):
        return JsonResponse({"error": "Se esperaba un objeto JSON"}, status=400)

    usuario = Usuario.objects.filter(id=id).first()
    if usuario is None:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    apodo = datos.get("apodo")
    if not isinstance(apodo, str) or not apodo.strip():
        return JsonResponse({"error": "El apodo es obligatorio"}, status=400)

    habilidad_arma = datos.get("habilidad_arma", 0)
    habilidad_conduccion = datos.get("habilidad_conduccion", 0)
    for valor in (habilidad_arma, habilidad_conduccion):
        if not isinstance(valor, int) or isinstance(valor, bool) or not 0 <= valor <= 100:
            return JsonResponse(
                {"error": "Las habilidades deben ser enteros entre 0 y 100"},
                status=400
            )

    capitan = datos.get("capitan", False)
    if not isinstance(capitan, bool):
        return JsonResponse({"error": "El campo capitan debe ser true o false"}, status=400)

    nombres = datos.get("caracteristicas", [])
    if not isinstance(nombres, list):
        return JsonResponse({"error": "caracteristicas debe ser una lista"}, status=400)

    caracteristicas = Caracteristica.objects.filter(nombre__in=nombres)
    if caracteristicas.count() != len(set(nombres)):
        return JsonResponse({"error": "Alguna característica no existe"}, status=400)

    usuario.apodo = apodo.strip()
    usuario.habilidad_arma = habilidad_arma
    usuario.habilidad_conduccion = habilidad_conduccion
    usuario.capitan = capitan
    usuario.save()
    usuario.caracteristicas.set(caracteristicas)

    return JsonResponse({"mensaje": "Usuario actualizado correctamente", "id": usuario.id})


@csrf_exempt
def eliminar_usuario(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    usuario = Usuario.objects.filter(id=id).first()
    if usuario is None:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    usuario.delete()
    return HttpResponse(status=204)

def listar_tripulantes_mision(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    mision = Mision.objects.filter(id=id).first()
    if mision is None:
        return JsonResponse({"error": "Misión no encontrada"}, status=404)

    participantes = mision.participantes.order_by("-capitan", "apodo")

    tripulacion = []
    for usuario in participantes:
        if usuario.capitan:
            funcion = "capitán"
        else:
            funcion = "tripulante"

        tripulacion.append({
            "id": usuario.id,
            "apodo": usuario.apodo,
            "funcion": funcion,
        })

    return JsonResponse({
        "mision": mision.nombre,
        "estado": mision.estado,
        "nave": mision.nave.nombre,
        "tripulacion": tripulacion,
    })

@csrf_exempt
def crear_mision(request):
    if request.method != "POST":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(datos, dict):
        return JsonResponse({"error": "Se esperaba un objeto JSON"}, status=400)

    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        return JsonResponse({"error": "El nombre es obligatorio"}, status=400)

    nave_id = datos.get("nave_id")
    if nave_id is None:
        return JsonResponse({"error": "La misión debe tener una nave"}, status=400)

    nave = Nave.objects.filter(id=nave_id).first()
    if nave is None:
        return JsonResponse({"error": "La nave no existe"}, status=400)

    ids = datos.get("participantes")
    if not isinstance(ids, list) or len(ids) == 0:
        return JsonResponse({"error": "participantes debe ser una lista de ids"}, status=400)

    for valor in ids:
        if not isinstance(valor, int) or isinstance(valor, bool):
            return JsonResponse({"error": "Los ids de participantes deben ser enteros"}, status=400)

    if len(ids) != len(set(ids)):
        return JsonResponse({"error": "Hay participantes repetidos"}, status=400)

    usuarios = Usuario.objects.filter(id__in=ids)
    if usuarios.count() != len(ids):
        return JsonResponse({"error": "Alguno de los participantes no existe"}, status=400)

    if len(ids) != nave.capacidad:
        return JsonResponse(
            {"error": "La nave necesita " + str(nave.capacidad) + " participantes y se han enviado " + str(len(ids))},
            status=400
        )

    capitanes = usuarios.filter(capitan=True).count()
    if capitanes != nave.capitanes_requeridos():
        return JsonResponse(
            {"error": "La nave necesita " + str(nave.capitanes_requeridos()) + " capitán(es) y se han enviado " + str(capitanes)},
            status=400
        )

    ocupados = usuarios.filter(misiones__estado="En curso").distinct()
    if ocupados.exists():
        apodos = list(ocupados.values_list("apodo", flat=True))
        return JsonResponse(
            {"error": "Hay usuarios ocupados en otra misión en curso", "ocupados": apodos},
            status=400
        )

    mision = Mision.objects.create(
        nombre=nombre.strip(),
        nave=nave,
        estado="En curso",
        fecha_inicio=date.today()
    )
    mision.participantes.set(usuarios)

    return JsonResponse(
        {"mensaje": "Misión creada correctamente", "id": mision.id},
        status=201
    )

@csrf_exempt
def finalizar_mision(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(datos, dict):
        return JsonResponse({"error": "Se esperaba un objeto JSON"}, status=400)

    mision = Mision.objects.filter(id=id).first()
    if mision is None:
        return JsonResponse({"error": "Misión no encontrada"}, status=404)

    # Una misión finalizada no se puede volver a finalizar
    if mision.estado != "En curso":
        return JsonResponse({"error": "La misión ya está finalizada"}, status=400)

    resultado = datos.get("resultado")
    if resultado not in ("Exitosa", "Fallida"):
        return JsonResponse(
            {"error": "resultado debe ser 'Exitosa' o 'Fallida'"},
            status=400
        )

    exoplanetas = datos.get("exoplanetas", [])
    if not isinstance(exoplanetas, list):
        return JsonResponse({"error": "exoplanetas debe ser una lista"}, status=400)

    # Solo se registran exoplanetas si la misión ha tenido éxito
    if resultado == "Fallida" and len(exoplanetas) > 0:
        return JsonResponse(
            {"error": "Una misión fallida no puede registrar exoplanetas"},
            status=400
        )

    # Validamos todos los exoplanetas ANTES de guardar nada
    nombres_vistos = []
    for exo in exoplanetas:
        if not isinstance(exo, dict):
            return JsonResponse({"error": "Cada exoplaneta debe ser un objeto JSON"}, status=400)

        nombre = exo.get("nombre")
        if not isinstance(nombre, str) or not nombre.strip() or len(nombre.strip()) > 100:
            return JsonResponse(
                {"error": "Cada exoplaneta necesita un nombre (máximo 100 caracteres)"},
                status=400
            )

        nombre = nombre.strip()
        if nombre in nombres_vistos:
            return JsonResponse({"error": "Nombre de exoplaneta repetido: " + nombre}, status=400)
        if Exoplaneta.objects.filter(nombre=nombre).exists():
            return JsonResponse({"error": "El exoplaneta ya existe: " + nombre}, status=400)

        descripcion = exo.get("descripcion")
        if descripcion is not None and not isinstance(descripcion, str):
            return JsonResponse({"error": "La descripción debe ser un texto"}, status=400)

        nombres_vistos.append(nombre)

    # Todo es válido: ahora sí guardamos
    mision.estado = resultado
    mision.fecha_fin = date.today()
    mision.save()

    creados = []
    for exo in exoplanetas:
        nuevo = Exoplaneta.objects.create(
            nombre=exo["nombre"].strip(),
            mision=mision,
            descripcion=exo.get("descripcion")
        )
        creados.append({"id": nuevo.id, "nombre": nuevo.nombre})

    return JsonResponse({
        "mensaje": "Misión finalizada correctamente",
        "id": mision.id,
        "estado": mision.estado,
        "fecha_fin": mision.fecha_fin.isoformat(),
        "exoplanetas": creados,
    })

def listar_exoplanetas_capitan(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Operación no permitida"}, status=405)

    usuario = Usuario.objects.filter(id=id).first()
    if usuario is None:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    if not usuario.capitan:
        return JsonResponse({"error": "El usuario no es capitán"}, status=400)

    exoplanetas = Exoplaneta.objects.filter(
        mision__participantes=usuario
    ).distinct().order_by("nombre")

    resultado = []
    for exo in exoplanetas:
        resultado.append({
            "id": exo.id,
            "nombre": exo.nombre,
            "descripcion": exo.descripcion,
            "fecha_descubrimiento": exo.fecha_descubrimiento.isoformat(),
            "mision": exo.mision.nombre,
        })

    return JsonResponse({
        "capitan": usuario.apodo,
        "exoplanetas": resultado,
    })