import random
from datetime import timedelta

from faker import Faker

from .models import Caracteristica, Usuario, Nave, Mision, Exoplaneta

fake = Faker('es_ES')


# Factoria para generar los datos de prueba (RF2).
# Cada funcion crea y guarda un objeto de un modelo con datos aleatorios.


def crear_caracteristicas():
    # Las caracteristicas son fijas, asi que se crean solo si no existen
    caracteristicas = []
    for opcion in Caracteristica.OPCIONES_CARACTERISTICA:
        caracteristica, creada = Caracteristica.objects.get_or_create(
            nombre=opcion[0],
            defaults={'descripcion': fake.sentence()}
        )
        caracteristicas.append(caracteristica)
    return caracteristicas


def crear_usuario(capitan=False):
    usuario = Usuario.objects.create(
        apodo=fake.user_name(),
        habilidad_arma=random.randint(0, 100),
        habilidad_conduccion=random.randint(0, 100),
        capitan=capitan
    )

    # A cada usuario le ponemos entre 0 y 3 caracteristicas distintas
    caracteristicas = list(Caracteristica.objects.all())
    cantidad = random.randint(0, 3)
    usuario.caracteristicas.set(random.sample(caracteristicas, cantidad))

    return usuario


def crear_nave(tamanio):
    # La capacidad depende del tamanio de la nave
    if tamanio == 'Pequeña':
        capacidad = 4
    elif tamanio == 'Mediana':
        capacidad = random.randint(8, 10)
    else:
        capacidad = random.randint(11, 30)

    nave = Nave.objects.create(
        nombre='Nave ' + fake.last_name() + ' ' + str(random.randint(1, 999)),
        tamanio=tamanio,
        capacidad=capacidad
    )
    return nave


def usuarios_ocupados():
    # Ids de los usuarios que estan ahora mismo en una mision en curso
    return Usuario.objects.filter(misiones__estado='En curso').values_list('id', flat=True)


def elegir_tripulacion(nave, en_curso):
    # Se llena la nave: los capitanes que le tocan y el resto tripulantes
    capitanes = Usuario.objects.filter(capitan=True)
    tripulantes = Usuario.objects.filter(capitan=False)

    # Si la mision va a estar en curso no se puede coger gente ocupada
    if en_curso:
        ocupados = list(usuarios_ocupados())
        capitanes = capitanes.exclude(id__in=ocupados)
        tripulantes = tripulantes.exclude(id__in=ocupados)

    num_capitanes = nave.capitanes_requeridos()
    num_tripulantes = nave.capacidad - num_capitanes

    capitanes = list(capitanes)
    tripulantes = list(tripulantes)

    if len(capitanes) < num_capitanes or len(tripulantes) < num_tripulantes:
        return None

    return random.sample(capitanes, num_capitanes) + random.sample(tripulantes, num_tripulantes)


def crear_mision(nave, estado):
    # estado puede ser 'En curso', 'Exitosa' o 'Fallida'
    en_curso = estado == 'En curso'

    tripulacion = elegir_tripulacion(nave, en_curso)
    if tripulacion is None:
        return None

    if en_curso:
        fecha_inicio = fake.date_between(start_date='-30d', end_date='today')
        fecha_fin = None
    else:
        fecha_inicio = fake.date_between(start_date='-2y', end_date='-60d')
        fecha_fin = fecha_inicio + timedelta(days=random.randint(5, 50))

    mision = Mision.objects.create(
        nombre='Expedicion ' + fake.city(),
        nave=nave,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    mision.participantes.set(tripulacion)

    return mision


def crear_exoplaneta(mision):
    # El nombre es unico, se repite hasta que salga uno que no exista
    nombre = fake.last_name() + '-' + str(random.randint(1, 999)) + random.choice(['b', 'c', 'd'])
    while Exoplaneta.objects.filter(nombre=nombre).exists():
        nombre = fake.last_name() + '-' + str(random.randint(1, 999)) + random.choice(['b', 'c', 'd'])

    exoplaneta = Exoplaneta.objects.create(
        nombre=nombre,
        mision=mision,
        descripcion=fake.sentence()
    )
    return exoplaneta