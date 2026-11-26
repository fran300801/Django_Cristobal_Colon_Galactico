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

### ⏳ Pendiente

- **API REST (RF3):** CRUD de usuarios, asignar misión, finalizar misión, consultar tripulantes de una misión y consultar los planetas descubiertos por un capitán.
- **Batería de pruebas:** Tests de modelos, endpoints y reglas de negocio.
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

⏳ La API REST todavía no está implementada. Aquí se documentará cada endpoint (método, ruta, descripción y body) con sus ejemplos de petición y respuesta JSON.

---

## 🧪 Pruebas

⏳ La batería de pruebas todavía no está implementada. Se ejecutará con:

```bash
python manage.py test
```

---

## 👥 Trabajo realizado

| Integrante           | Trabajo                                                    |
| -------------------- | ---------------------------------------------------------- |
| Francisco José       | Estructura del proyecto y modelos `Usuario`, `Nave` y `Mision`. |
| Alberto García Moreno  | Modelos `Exoplaneta` y `Caracteristica`. |
| Alberto García Moreno |    Factoría y comando de datos de prueba (RF2).               |
|  Francisco José Sobrino       |    Desarrollo De Api REST         |

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

---