# 🚀 Cristóbal Colón Galáctico API (Django)

Este proyecto es el desarrollo de una aplicación **back-end con Django** que gestiona misiones espaciales destinadas a la **exploración y descubrimiento de exoplanetas**.

La aplicación administra los **usuarios** de las expediciones (capitanes y tripulantes), las **naves espaciales** según su tamaño y capacidad, las **misiones** en las que participan y los **exoplanetas** descubiertos cuando una misión termina con éxito.  
Además, cada usuario tiene una serie de **características** (misiones largas, cocinero, mantenimiento, etc.) que definen su perfil dentro de la tripulación.

## ✒️ Autores

- **Francisco José Sobrino**
  - GitHub: `https://github.com/fran300801`
- **Alberto García Moreno**
  - GitHub: `https://github.com/Alberto21-21`

---

## 🎯 Objetivos que cumple

- **Modelos (RF1):** Usuarios, naves, misiones, exoplanetas y características, con sus relaciones.
- **Tipos de nave:** Pequeña (4 tripulantes), mediana (entre 8 y 10) y grande (entre 11 y 30).
- **Capitanes por nave:** Las naves pequeñas y medianas llevan un capitán y las grandes dos.
- **Exoplanetas solo con éxito:** No se puede guardar un exoplaneta en una misión que no haya tenido éxito.
- **Factoría de datos (RF2):** Comando que genera datos de prueba aleatorios con Faker respetando las restricciones anteriores.
- **API REST (RF3):** CRUD completo de usuarios, consulta de tripulantes de una misión, creación de misiones validando capacidad/capitanes/disponibilidad, finalización de misiones con registro de exoplanetas y consulta de exoplanetas descubiertos por un capitán.
- **Batería de pruebas:** 21 tests unitarios y de integración que validan los modelos, los endpoints de la API REST y las reglas de negocio.

### ⏳ Pendiente

- **Despliegue.**

---

## 🗃️ Modelos

| Modelo           | Campos principales                                                          | Relaciones                                    |
| ---------------- | --------------------------------------------------------------------------- | --------------------------------------------- |
| `Caracteristica` | `nombre` (único, 5 opciones), `descripcion`                                 | —                                             |
| `Usuario`        | `apodo`, `habilidad_arma`, `habilidad_conduccion`, `capitan`                | Muchos a muchos con `Caracteristica`          |
| `Nave`           | `nombre`, `tamanio`, `capacidad`                                            | —                                             |
| `Mision`         | `nombre`, `estado`, `fecha_inicio`, `fecha_fin`                             | Una `Nave` (FK) y muchos `Usuario` (M2M)      |
| `Exoplaneta`     | `nombre` (único), `fecha_descubrimiento`, `descripcion`                     | Una `Mision` (FK)                             |

### Estados de una misión

| Estado     | Significado                                              |
| ---------- | -------------------------------------------------------- |
| `En curso` | La misión no ha terminado. Sus usuarios están ocupados.  |
| `Exitosa`  | Misión finalizada con éxito. Puede tener exoplanetas.    |
| `Fallida`  | Misión finalizada sin éxito. No puede tener exoplanetas. |

---

## ⚙️ Ejemplos de ejecución y funcionamiento

### Carga de datos de prueba (factoría)

Para poblar la base de datos con datos de prueba se utiliza el siguiente comando de gestión:

```bash
# Genera los datos de prueba
python manage.py generar_datos

# Borra los datos anteriores y genera otros nuevos
python manage.py generar_datos --borrar
```

El comando usa las funciones de la factoría (`cristobalcolon/factories.py`) y crea:

| Datos        | Cantidad | Detalle                                                             |
| ------------ | -------- | ------------------------------------------------------------------- |
| Usuarios     | 70       | 10 capitanes y 60 tripulantes, con entre 0 y 3 características.     |
| Naves        | 7        | 3 pequeñas, 2 medianas y 2 grandes, con la capacidad de su tamaño.  |
| Misiones     | 10       | 4 exitosas, 3 fallidas y 3 en curso.                                |
| Exoplanetas  | Variable | Entre 1 y 3 por cada misión exitosa.                                |

Los datos generados respetan las reglas del proyecto:

- Cada misión lleva la nave llena y con los capitanes que le corresponden.
- Ningún usuario está en dos misiones en curso a la vez.
- Solo las misiones exitosas tienen exoplanetas.

Ejemplo de salida:

```bash
Datos de prueba generados:
Usuarios: 70
Naves: 7
Misiones: 10
Misiones en curso: 3
Exoplanetas: 8
```

---

## 🧩 Tabla de Endpoints

Todos los endpoints cuelgan del prefijo `/api/`.

| Método   | Ruta                                     | Descripción                                                         | Body JSON esperado                                                                                                                               | Respuesta principal      |
| -------- | ---------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| `GET`    | `/api/usuarios/`                         | Lista todos los usuarios con sus características.                   | —                                                                                                                                                | `200 OK` (lista)         |
| `GET`    | `/api/usuarios/<int:id>/`                | Obtiene el detalle de un usuario por su ID.                         | —                                                                                                                                                | `200 OK` / `404`         |
| `POST`   | `/api/usuarios/crear/`                   | Crea un nuevo usuario y asigna sus características.                 | `{"apodo": "Nova", "habilidad_arma": 70, "habilidad_conduccion": 85, "capitan": true, "caracteristicas": ["Misiones largas"]}`                   | `201 Created`            |
| `PUT`    | `/api/usuarios/<int:id>/actualizar/`     | Actualiza por completo los datos y características de un usuario.   | `{"apodo": "Nova", "habilidad_arma": 75, "habilidad_conduccion": 90, "capitan": true, "caracteristicas": ["Misiones largas", "Mantenimiento"]}` | `200 OK` / `404`         |
| `DELETE` | `/api/usuarios/<int:id>/eliminar/`       | Elimina un usuario por su ID.                                       | —                                                                                                                                                | `204 No Content`         |
| `GET`    | `/api/misiones/<int:id>/tripulantes/`    | Lista los tripulantes y capitanes de una misión (ordenados).        | —                                                                                                                                                | `200 OK` / `404`         |
| `POST`   | `/api/misiones/crear/`                   | Crea una misión `En curso` validando capacidad, capitanes y libres. | `{"nombre": "Odisea I", "nave_id": 1, "participantes": [1, 2, 3, 4]}`                                                                             | `201 Created` / `400`    |
| `POST`   | `/api/misiones/<int:id>/finalizar/`      | Finaliza una misión (`Exitosa` o `Fallida`) y registra exoplanetas. | `{"resultado": "Exitosa", "exoplanetas": [{"nombre": "Kepler-X", "descripcion": "Habitable"}]}`                                                 | `200 OK` / `400`         |
| `GET`    | `/api/capitanes/<int:id>/exoplanetas/`   | Lista los exoplanetas descubiertos en misiones de un capitán.       | —                                                                                                                                                | `200 OK` / `400` / `404` |

### Ejemplos de petición y respuesta JSON

#### Crear usuario (`POST /api/usuarios/crear/`)

Petición:
```json
{
  "apodo": "EstrellaFugaz",
  "habilidad_arma": 60,
  "habilidad_conduccion": 80,
  "capitan": false,
  "caracteristicas": ["Cocinero", "Mantenimiento"]
}
```
Respuesta (`201 Created`):
```json
{
  "mensaje": "Usuario creado correctamente",
  "id": 71
}
```

#### Consultar tripulantes de una misión (`GET /api/misiones/1/tripulantes/`)

Respuesta (`200 OK`):
```json
{
  "mision": "Exploración Orión",
  "estado": "En curso",
  "nave": "Halcón Galáctico",
  "tripulacion": [
    {
      "id": 1,
      "apodo": "CapitanVega",
      "funcion": "capitán"
    },
    {
      "id": 2,
      "apodo": "Tripulante02",
      "funcion": "tripulante"
    }
  ]
}
```

#### Crear misión (`POST /api/misiones/crear/`)

Petición:
```json
{
  "nombre": "Rumbo Andrómeda",
  "nave_id": 1,
  "participantes": [1, 2, 3, 4]
}
```
Respuesta (`201 Created`):
```json
{
  "mensaje": "Misión creada correctamente",
  "id": 11
}
```

#### Finalizar misión (`POST /api/misiones/11/finalizar/`)

Petición:
```json
{
  "resultado": "Exitosa",
  "exoplanetas": [
    {
      "nombre": "Aethelgard-4",
      "descripcion": "Mundo oceánico con atmósfera estable"
    }
  ]
}
```
Respuesta (`200 OK`):
```json
{
  "mensaje": "Misión finalizada correctamente",
  "id": 11,
  "estado": "Exitosa",
  "fecha_fin": "2026-11-27",
  "exoplanetas": [
    {
      "id": 9,
      "nombre": "Aethelgard-4"
    }
  ]
}
```

#### Exoplanetas de un capitán (`GET /api/capitanes/1/exoplanetas/`)

Respuesta (`200 OK`):
```json
{
  "capitan": "CapitanVega",
  "exoplanetas": [
    {
      "id": 9,
      "nombre": "Aethelgard-4",
      "descripcion": "Mundo oceánico con atmósfera estable",
      "fecha_descubrimiento": "2026-11-27",
      "mision": "Rumbo Andrómeda"
    }
  ]
}
```

---

## 🧪 Pruebas

La batería de pruebas está implementada en `cristobalcolon/tests.py` con **21 tests** organizados en 4 clases:

| Clase de Test         | Qué comprueba                                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `ModelosTest`         | Capacidad válida según tamaño de nave, capitanes requeridos, asignación de características y restricción de exoplanetas.     |
| `UsuariosAPITest`     | Operaciones CRUD completas sobre los endpoints de usuarios (`listar`, `detalle`, `crear`, `actualizar` y `eliminar`).         |
| `MisionesAPITest`     | Creación válida de misiones, validaciones (sin nave, tripulación incompleta, sin capitán, usuarios ocupados) y finalización. |
| `ExoplanetasAPITest`  | Consulta de exoplanetas descubiertos por un capitán y errores cuando el usuario no es capitán o no existe.                    |

Para ejecutar toda la batería de pruebas:

```bash
python manage.py test
```

Ejemplo de salida:

```bash
Found 21 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.245s

OK
Destroying test database for alias 'default'...
```

---

## 👥 Trabajo realizado

| Integrante             | Trabajo                                                       |
| ---------------------- | ------------------------------------------------------------- |
| Francisco José Sobrino | Estructura del proyecto y modelos `Usuario`, `Nave` y `Mision`. |
| Alberto García Moreno  | Modelos `Exoplaneta` y `Caracteristica`.                    |
| Alberto García Moreno  | Factoría y comando de datos de prueba (RF2).                  |
| Francisco José Sobrino | Desarrollo de API REST (RF3).                                 |
| Francisco José Sobrino | Batería de tests.                                             |

---

## 🏗️ Tecnologías utilizadas

```bash
- Python 3.13
- Django 6.1
- Faker
- SQLite
```

---

## 🚀 Ejecución del proyecto

```bash
# 1. Clona el repositorio
git clone https://github.com/fran300801/Django_Cristobal_Colon_Galactico.git
cd Django_Cristobal_Colon_Galactico

# 2. Crea y activa el entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Crea y aplica las migraciones
python manage.py makemigrations cristobalcolon
python manage.py migrate

# 5. Genera los datos de prueba
python manage.py generar_datos

# 6. Ejecuta el servidor
python manage.py runserver
```

---

## 📚 Licencia

- Este proyecto se distribuye bajo la licencia MIT.
- Eres libre de usarlo y modificarlo, siempre que se mantenga la atribución original.