from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    # organizaciones
    path('', views.inicio, name="inicio"),
    path('organizacion/<int:id_org>/', views.tabs_organizacion, name = "tabs_organizacion"),
    path('form_organizacion/', views.agregar_organizacion, name = "form_organizacion"),
    path('buscar_org/', views.buscar_organizacion, name = "buscar_organizacion"), 
    path('agregar_org/', views.agregar_org, name = "agregar_org"),
    
    #sitios
    path('sitios/', views.sitios, name = "sitios"),
    path('sitios/<int:id_site>/', views.tabs_sitios, name = "tabs_sitios"),
    path('agregar_sitio/', views.agregar_sitio, name = "agregar_sitio"),
    path('agregar_site/', views.agregar_site, name = "agregar_site"),
    path('buscar_sitio/', views.buscar_sitio, name = "buscar_sitio"),
    
    #Personas
    path('personas/', views.personas, name = "personas"),
    path('buscar_personas/', views.buscar_personas, name = "buscar_persona"),
    path('form_persona/', views.form_persona, name = "form_persona"),
    path('agregar_persona/', views.agregar_persona, name = "agregar_persona"),
    path('actualizar_persona/<str:id_persona>/', views.actualizar_persona, name = "actualizar_persona"),
    path('update_persona/<str:id_persona>/', views.update_persona, name = "update_persona"),
    path('permisos_persona/<str:id_persona>/', views.permisos_persona, name = "permisos_persona"),
    path('eliminar_permiso/<str:id_persona>/<int:id_permiso>/', views.eliminar_permiso, name="eliminar_permiso"),
    path('modificar_permiso/<str:id_persona>/<int:id_permiso>/', views.modificar_permiso, name="modificar_permiso"),
    path('formulario_permisos/<str:id_persona>/', views.formulario_permisos, name = "formulario_permisos"),
    path('guardar_permiso/<str:id_persona>', views.guardar_permiso, name="guardar_permiso"),
    path('guardar_modificar_permiso/<str:id_persona>/<int:id_permiso>', views.guardar_modificar_permiso, name = "guardar_modificar_permiso"),
    
    #Dispositivos
    path('dispositivos/', views.dispositivos, name = "dispositivos"),
    path('buscar_dispositivos/', views.buscar_dispositivos, name = 'buscar_dispositivos'),
    path('form_dispositivo/', views.form_dispositivo, name = "form_dispositivo"),
    path('agregar_dispositivo/', views.agregar_dispositivo, name = "agregar_dispositivo"),
    path('formulario_actualizar_dispositivo/<int:id_device>/', views.formulario_actualizar_dispositivo, name="formulario_actualizar_dispositivo"),
    path('actualizar_dispositivo/<int:id_device>/', views.actualizar_dispositivo, name ="actualizar_dispositivo"),
    path('eliminar_dispositivo/<int:id_device>/', views.eliminar_dispositivo, name = "eliminar_dispositivo"),
    
]
