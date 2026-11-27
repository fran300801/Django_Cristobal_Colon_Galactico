from django.test import TestCase
from django.core.exceptions import ValidationError
import json
from django.urls import reverse
from .models import Usuario, Nave, Mision, Exoplaneta, Caracteristica

# Create your tests here.

class ModelosTest(TestCase):

    # TEST 1: Comprobar la capacidad de las naves
    def test_capacidad_valida(self):

        nave_pequena = Nave(nombre='Nave pequeña', tamanio='Pequeña', capacidad=4)
        nave_mediana = Nave(nombre='Nave mediana', tamanio='Mediana', capacidad=8)
        nave_grande = Nave(nombre='Nave grande', tamanio='Grande', capacidad=15)

        self.assertTrue(nave_pequena.capacidad_valida())
        self.assertTrue(nave_mediana.capacidad_valida())
        self.assertTrue(nave_grande.capacidad_valida())

        nave_invalida = Nave(nombre='Nave inválida', tamanio='Pequeña', capacidad=10)

        self.assertFalse(nave_invalida.capacidad_valida())

    # TEST 2: Comprobar el número de capitanes necesarios
    def test_capitanes_requeridos(self):

        nave_pequena = Nave(nombre='Nave pequeña', tamanio='Pequeña', capacidad=4)
        nave_mediana = Nave(nombre='Nave mediana', tamanio='Mediana', capacidad=8)
        nave_grande = Nave(nombre='Nave grande', tamanio='Grande', capacidad=15)

        self.assertEqual(nave_pequena.capitanes_requeridos(), 1)
        self.assertEqual(nave_mediana.capitanes_requeridos(), 1)
        self.assertEqual(nave_grande.capitanes_requeridos(), 2)

    # TEST 3: Comprobar la relación entre usuarios y características
    def test_usuario_puede_tener_caracteristicas(self):

        usuario = Usuario.objects.create(apodo='Explorador')

        caracteristica1 = Caracteristica.objects.create(
            nombre='Misiones largas'
        )

        caracteristica2 = Caracteristica.objects.create(
            nombre='Mantenimiento'
        )

        usuario.caracteristicas.add(caracteristica1, caracteristica2)

        self.assertEqual(usuario.caracteristicas.count(), 2)
        self.assertIn(caracteristica1, usuario.caracteristicas.all())
        self.assertIn(caracteristica2, usuario.caracteristicas.all())

    # TEST 4: No permitir exoplanetas en misiones sin éxito
    def test_no_permitir_exoplaneta_mision_no_exitosa(self):

        nave = Nave.objects.create(
            nombre='Cristóbal Colón',
            tamanio='Pequeña',
            capacidad=4
        )

        mision = Mision.objects.create(
            nombre='Exploración fallida',
            nave=nave,
            estado='En curso'
        )

        exoplaneta = Exoplaneta(
            nombre='Kepler-452b',
            mision=mision
        )

        with self.assertRaises(ValidationError):
            exoplaneta.save()

    # TEST 5: Permitir exoplanetas en misiones exitosas
    def test_permitir_exoplaneta_mision_exitosa(self):

        nave = Nave.objects.create(
            nombre='Cristóbal Colón',
            tamanio='Pequeña',
            capacidad=4
        )

        mision = Mision.objects.create(
            nombre='Exploración exitosa',
            nave=nave,
            estado='Exitosa'
        )

        exoplaneta = Exoplaneta.objects.create(
            nombre='Kepler-452b',
            mision=mision
        )

        self.assertEqual(Exoplaneta.objects.count(), 1)
        self.assertEqual(exoplaneta.mision, mision)


class UsuariosAPITest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            apodo='Explorador',
            habilidad_arma=70,
            habilidad_conduccion=80,
            capitan=False
        )

    # TEST 6: Listar todos los usuarios
    def test_listar_usuarios(self):

        respuesta = self.client.get(reverse('listar_usuarios'))

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        self.assertEqual(len(datos), 1)
        self.assertEqual(datos[0]['apodo'], 'Explorador')

    # TEST 7: Consultar un usuario concreto
    def test_listar_usuario_concreto(self):

        respuesta = self.client.get(
            reverse('usuario_concreto', args=[self.usuario.id])
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()['apodo'], 'Explorador')

    # TEST 8: Crear un usuario
    def test_crear_usuario(self):

        datos = {
            'apodo': 'Piloto',
            'habilidad_arma': 50,
            'habilidad_conduccion': 90,
            'capitan': True,
            'caracteristicas': []
        }

        respuesta = self.client.post(
            reverse('crear_usuario'),
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 201)
        self.assertTrue(Usuario.objects.filter(apodo='Piloto').exists())

    # TEST 9: Actualizar un usuario
    def test_actualizar_usuario(self):

        datos = {
            'apodo': 'Explorador actualizado',
            'habilidad_arma': 90,
            'habilidad_conduccion': 60,
            'capitan': True,
            'caracteristicas': []
        }

        respuesta = self.client.put(
            reverse('actualizar_usuario', args=[self.usuario.id]),
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 200)

        self.usuario.refresh_from_db()

        self.assertEqual(self.usuario.apodo, 'Explorador actualizado')
        self.assertEqual(self.usuario.habilidad_arma, 90)
        self.assertTrue(self.usuario.capitan)

    # TEST 10: Eliminar un usuario
    def test_eliminar_usuario(self):

        respuesta = self.client.delete(
            reverse('eliminar_usuario', args=[self.usuario.id])
        )

        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(
            Usuario.objects.filter(id=self.usuario.id).exists()
        )


class MisionesAPITest(TestCase):

    def setUp(self):
        self.nave = Nave.objects.create(
            nombre='Cristóbal Colón',
            tamanio='Pequeña',
            capacidad=4
        )

        self.usuarios = []

        for i in range(4):
            usuario = Usuario.objects.create(
                apodo=f'Explorador{i}',
                capitan=(i == 0)
            )
            self.usuarios.append(usuario)

        self.datos_mision = {
            'nombre': 'Exploración de Kepler',
            'nave_id': self.nave.id,
            'participantes': [u.id for u in self.usuarios]
        }

    # TEST 11: Crear una misión correctamente
    def test_crear_mision(self):

        respuesta = self.client.post(
            reverse('crear_mision'),
            data=json.dumps(self.datos_mision),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Mision.objects.count(), 1)

        mision = Mision.objects.first()

        self.assertEqual(mision.nombre, 'Exploración de Kepler')
        self.assertEqual(mision.participantes.count(), 4)
        self.assertEqual(mision.estado, 'En curso')

    # TEST 12: Impedir crear una misión sin nave
    def test_crear_mision_sin_nave(self):

        datos = self.datos_mision.copy()
        del datos['nave_id']

        respuesta = self.client.post(
            reverse('crear_mision'),
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 0)

    # TEST 13: Impedir crear una misión con tripulación incompleta
    def test_crear_mision_tripulacion_incompleta(self):

        datos = self.datos_mision.copy()
        datos['participantes'] = [u.id for u in self.usuarios[:3]]

        respuesta = self.client.post(
            reverse('crear_mision'),
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 0)

    # TEST 14: Impedir crear una misión sin los capitanes necesarios
    def test_crear_mision_sin_capitan(self):

        for usuario in self.usuarios:
            usuario.capitan = False
            usuario.save()

        respuesta = self.client.post(
            reverse('crear_mision'),
            data=json.dumps(self.datos_mision),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 0)

    # TEST 15: Impedir asignar usuarios ocupados
    def test_crear_mision_usuario_ocupado(self):

        mision_anterior = Mision.objects.create(
            nombre='Misión anterior',
            nave=self.nave,
            estado='En curso'
        )

        mision_anterior.participantes.add(self.usuarios[0])

        respuesta = self.client.post(
            reverse('crear_mision'),
            data=json.dumps(self.datos_mision),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 1)

    # TEST 16: Consultar los tripulantes de una misión
    def test_listar_tripulantes(self):

        mision = Mision.objects.create(
            nombre='Exploración de Kepler',
            nave=self.nave
        )

        mision.participantes.set(self.usuarios)

        respuesta = self.client.get(
            reverse('tripulantes_mision', args=[mision.id])
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        self.assertEqual(datos['mision'], 'Exploración de Kepler')
        self.assertEqual(len(datos['tripulacion']), 4)

        capitan = datos['tripulacion'][0]

        self.assertEqual(capitan['apodo'], 'Explorador0')
        self.assertEqual(capitan['funcion'], 'capitán')

    # TEST 17: Finalizar una misión con éxito y registrar exoplanetas
    def test_finalizar_mision_exitosa(self):

        mision = Mision.objects.create(
            nombre='Exploración exitosa',
            nave=self.nave
        )

        datos = {
            'resultado': 'Exitosa',
            'exoplanetas': [
                {
                    'nombre': 'Kepler-452b',
                    'descripcion': 'Planeta descubierto'
                }
            ]
        }

        respuesta = self.client.post(
            reverse('finalizar_mision', args=[mision.id]),
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 200)

        mision.refresh_from_db()

        self.assertEqual(mision.estado, 'Exitosa')
        self.assertEqual(Exoplaneta.objects.count(), 1)
        self.assertEqual(
            Exoplaneta.objects.first().nombre,
            'Kepler-452b'
        )

    # TEST 18: Impedir registrar planetas en una misión fallida
    def test_finalizar_mision_fallida_con_exoplanetas(self):

        mision = Mision.objects.create(
            nombre='Exploración fallida',
            nave=self.nave
        )

        datos = {
            'resultado': 'Fallida',
            'exoplanetas': [
                {'nombre': 'Kepler-999b'}
            ]
        }

        respuesta = self.client.post(
            reverse('finalizar_mision', args=[mision.id]),
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 400)

        mision.refresh_from_db()

        self.assertEqual(mision.estado, 'En curso')
        self.assertEqual(Exoplaneta.objects.count(), 0)

class ExoplanetasAPITest(TestCase):
    def test_listar_exoplanetas_capitan(self):
        capitan = Usuario.objects.create(
            apodo="CapitanTest",
            capitan=True
        )

        nave = Nave.objects.create(
            nombre="NaveTest",
            tamanio="Pequeña",
            capacidad=4
        )

        mision = Mision.objects.create(
            nombre="MisionTest",
            nave=nave,
            estado="Exitosa"
        )
        mision.participantes.add(capitan)

        Exoplaneta.objects.create(
            nombre="PlanetaTest",
            mision=mision,
            descripcion="Planeta de prueba"
        )

        respuesta = self.client.get(
            reverse('exoplanetas_capitan', args=[capitan.id])
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        self.assertEqual(datos['capitan'], "CapitanTest")
        self.assertEqual(len(datos['exoplanetas']), 1)
        self.assertEqual(datos['exoplanetas'][0]['nombre'], "PlanetaTest")

    def test_listar_exoplanetas_usuario_no_capitan(self):
        usuario = Usuario.objects.create(
            apodo="UsuarioTest",
            capitan=False
        )

        respuesta = self.client.get(
            reverse('exoplanetas_capitan', args=[usuario.id])
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(
            respuesta.json()['error'],
            "El usuario no es capitán"
        )

    def test_listar_exoplanetas_usuario_inexistente(self):
        respuesta = self.client.get(
            reverse('exoplanetas_capitan', args=[9999])
        )

        self.assertEqual(respuesta.status_code, 404)
        self.assertEqual(
            respuesta.json()['error'],
            "Usuario no encontrado"
        )