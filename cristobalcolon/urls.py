from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("usuarios/<int:id>/", views.listar_usuario_concreto, name="usuario_concreto"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:id>/actualizar/", views.actualizar_usuario, name="actualizar_usuario"),
    path("usuarios/<int:id>/eliminar/", views.eliminar_usuario, name="eliminar_usuario"),
    path("misiones/<int:id>/tripulantes/", views.listar_tripulantes_mision, name="tripulantes_mision"),
    path("misiones/crear/", views.crear_mision, name="crear_mision"),
    path("misiones/<int:id>/finalizar/", views.finalizar_mision, name="finalizar_mision"),
    path("capitanes/<int:id>/exoplanetas/", views.listar_exoplanetas_capitan, name="exoplanetas_capitan"),

]