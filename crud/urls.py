from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    # organizaciones
    path('', views.inicio, name="inicio"),
    path('consulta/', views.consulta, name = "consulta"),
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
    
    #Dispositivos
    path('dispositivos/', views.dispositivos, name = "dispositivos"),
    path('buscar_dispositivos/', views.buscar_dispositivos, name = 'buscar_dispositivos'),
    path('form_dispositivo/', views.form_dispositivo, name = "form_dispositivo"),
    path('agregar_dispositivo/', views.agregar_dispositivo, name = "agregar_dispositivo"),
    path('actualizar_dispositivo/<int:id_device>/', views.actualizar_dispositivo, name="actualizar_dispositivo"),
    
    
    ##########################################################################################
    # eliminar elementos
    path('delete_org/<int:id_org>/', views.delete_org, name = "delete_org"),
    path('delete_employed/<int:id_people>/', views.delete_employed, name = "delete_employed"),
    path('delete_device/<int:id_device>/', views.delete_device, name = "delete_device"),
    
    # Template actualizar organizaciones
    path('update_org/<int:id_org>/', views.update_org, name = "update_org"),
    path('u_org/<int:id_org>/', views.u_org, name = "u_org"),
    
    # Template actualizar empleados
    path('update_emp/<int:id_emp>/', views.update_emp, name = "update_emp"),
    path('u_emp/<int:id_emp>/', views.u_emp, name = "u_emp"),
    
    # Template actualizar equipos
    path('update_dev/<int:id_dev>/', views.update_dev, name = "update_dev"),
    path('u_dev/<int:id_dev>/', views.u_dev, name = "u_dev"),
    
    # MENU
    # Agregar organizaciones
    path('registro_org/', views.register_org, name = "registro_org"),
    #path('neworg/', views.new_org, name = "neworg"),
    
    # Agregar Empleados
    path('registro_empleados/', views.register_employed, name = "registro_empleados"),
    path('newemployed/', views.new_employed, name = "newemployed"),
    
    # Agregar activos
    path('registro_activos/', views.register_device, name = "registro_activos"),
    path('newdevice/', views.new_device, name = "newdevice"),
    
    # Agregar zonas
    path('registro_zonas/', views.register_zone, name = "registro_zonas"),
    path('newzone/', views.new_zone, name = "newzone"),
    
    # Agregar Sitios
    #path('registro_sitios/', views.register_site, name = "registro_sitios"),
    #path('newsite/', views.new_site, name = "newsite"),
    
]
