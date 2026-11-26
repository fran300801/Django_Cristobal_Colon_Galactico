import random

from django.core.management.base import BaseCommand

from cristobalcolon.models import Usuario, Nave, Mision, Exoplaneta
from cristobalcolon import factories


class Command(BaseCommand):
    help = 'Comando de carga de datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--borrar',
            action='store_true',
            help='Borra los datos que hubiera antes de generar los nuevos'
        )

    def handle(self, *args, **options):
        if options['borrar']:
            # Primero los exoplanetas y misiones porque la nave esta protegida (PROTECT)
            Exoplaneta.objects.all().delete()
            Mision.objects.all().delete()
            Nave.objects.all().delete()
            Usuario.objects.all().delete()
            self.stdout.write('Datos anteriores borrados')

        # 1. Caracteristicas
        factories.crear_caracteristicas()

        # 2. Usuarios: 10 capitanes y 60 tripulantes
        for i in range(10):
            factories.crear_usuario(capitan=True)
        for i in range(60):
            factories.crear_usuario(capitan=False)

        # 3. Naves de los tres tamanios
        naves = []
        for i in range(3):
            naves.append(factories.crear_nave('Pequeña'))
        for i in range(2):
            naves.append(factories.crear_nave('Mediana'))
        for i in range(2):
            naves.append(factories.crear_nave('Grande'))

        # 4. Misiones finalizadas (con exito y sin exito) con naves al azar
        for i in range(4):
            mision = factories.crear_mision(random.choice(naves), 'Exitosa')

            # 5. Solo las misiones con exito tienen exoplanetas (entre 1 y 3)
            if mision is not None:
                for j in range(random.randint(1, 3)):
                    factories.crear_exoplaneta(mision)

        for i in range(3):
            factories.crear_mision(random.choice(naves), 'Fallida')

        # 6. Misiones en curso: una nave de cada tamanio.
        # La factoria solo coge usuarios que no esten ya en otra mision en curso
        factories.crear_mision(naves[0], 'En curso')
        factories.crear_mision(naves[3], 'En curso')
        factories.crear_mision(naves[5], 'En curso')

        self.stdout.write('Datos de prueba generados:')
        self.stdout.write('Usuarios: ' + str(Usuario.objects.count()))
        self.stdout.write('Naves: ' + str(Nave.objects.count()))
        self.stdout.write('Misiones: ' + str(Mision.objects.count()))
        self.stdout.write('Misiones en curso: ' + str(Mision.objects.filter(estado='En curso').count()))
        self.stdout.write('Exoplanetas: ' + str(Exoplaneta.objects.count()))