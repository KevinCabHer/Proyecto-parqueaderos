from multiprocessing import context
import re
from statistics import mode
from sys import orig_argv
from django.shortcuts import render, HttpResponse, redirect
from . import models
import datetime

#------------------#
#  Organizaciones  #
#------------------#

# Template Inicio: muestra la totaldiad de las Organizaciones
def inicio(request):
    
    organizaciones = models.tb_org.objects.all().values_list(named=True).exclude(org_name = "Sin organizacion")
    context = {"organizaciones": organizaciones}
    
    return render(request, 'organizaciones/organizaciones.html', context)

# Busca cualquier organización que contenga en su nombre texto de la busqueda
def buscar_organizacion(request):
    
    org = request.POST['buscar_organizacion']
    organizacion = models.tb_org.objects.filter(org_name__contains = org)
    
    context = {
        "organizaciones":organizacion
    }
    
    return render(request, 'organizaciones/organizaciones.html', context)

# Muestra el tabs de organizaciones con la informacion de sitios, zonas, equipos y personas relacionadas a la org
def tabs_organizacion(request, id_org):
    
    organizaciones = models.tb_org.objects.filter(id_org = id_org).values_list(named = True)
    personas = models.tb_people.objects.filter(id_org = id_org).values_list(named = True)
    sites = models.tb_sites.objects.filter(id_org = id_org).values()
    
    # ID DE LOS SITIOS
    id_sites = []
    for site in sites:
        if site.get('id_site') not in id_sites: 
            id_sites.append(site.get('id_site'))
     
     # ZONAS ADJUNTAS A LOS ID SITES
    zonas = {} 
    id_zonas = []      
    for id in id_sites:
        zona = models.tb_zones.objects.filter(id_site = id).values_list(named=True)
        zonas["id"] = zona
        for z in zona:
            id_zonas.append(z.id_zone)
    
    # EQUIPOS ADJUNTOS
    devices = {}
    for id in id_zonas:
        device = models.tb_devices.objects.select_related('id_cpu', 'id_os', 'id_device_type').filter(id_zone = id)
        devices[id] = device
    
    context = {
        "org": organizaciones,
        "people": personas,
        "zonas": zonas,
        "sites": sites,
        "devices": devices
    }
    
    return render(request, 'organizaciones/tabs_organizacion.html', context)



def agregar_organizacion(request):    
    context = {}
    return render(request, 'organizaciones/formulario_organizaciones.html', context)

# Agregar nuevas organizaciones
def agregar_org(request):
    
    # Datos del formulario Organizaciones
    nombre  = request.POST['name']
    id_tag  = request.POST['id_tag']
    country = request.POST['country']
    city    = request.POST['city']
    address = request.POST['address']
    postal  = request.POST['postal']
    
    # Instancia de la tabla tb_org con los datos necesarios para crear una nueva organización
    org = models.tb_org(org_name = nombre, org_tax_id = id_tag, country = country, city = city, addres = address, postal = postal)
    org.save()
    
    # Organizaciones 
    organizaciones = models.tb_org.objects.all().values_list(named=True)
    context = {"organizaciones": organizaciones}
    
    return redirect('/')

#------------#
#   Sitios   #
#------------#

# Muestra el template de sitios con la totalidad de sitios disponibles
def sitios(request):
    sites = models.tb_sites.objects.all().exclude(site_name = "Sin sitio")
    context = {'sites':sites}
    return render(request, 'sitios/sitios.html', context)

# Información del sitio consultado
def tabs_sitios(request, id_site):
    
    site = models.tb_sites.objects.filter(id_site = id_site).values()
    zones = models.tb_zones.objects.filter(id_site = id_site).values()
    
    # EQUIPOS ADJUNTOS
    devices = {}
    for zone in zones:
        device = models.tb_devices.objects.select_related('id_cpu', 'id_os', 'id_device_type').filter(id_zone = zone.get('id_zone'))
        devices[zone.get('id_zone')] = device
    
    context = {"site":site,"zones": zones,"devices":devices}
    
    return render(request, 'sitios/tabs_sitios.html', context)

# Buscar sitios
def buscar_sitio(request):
    name = request.POST['buscar_site']
    print(name)
    site = models.tb_sites.objects.filter(site_name__contains = name)
    context = {'sites':site}
    return render(request, 'sitios/sitios.html', context)    

# Mostrar template agregar sitio
def agregar_sitio(request):

    return render(request, 'sitios/formulario_sitios.html',)

# Agregar sitio
def agregar_site(request):
    
    nombre  = request.POST['name']
    country = request.POST['country']
    city    = request.POST['city']
    address = request.POST['address']
    postal  = request.POST['postal']
    
    site = models.tb_sites(site_name = nombre, country = country, city = city, address = address, postal = postal)
    site.save()

    sites = models.tb_sites.objects.all()
    context = {'sites':sites}
    
    return redirect('/sitios/')

#------------#
#  PERSONAS  #
#------------#

# Muestra el template con la totalidad de las personas
def personas(request):
    
    personas = models.tb_people.objects.all()
    context = {'personas':personas}
    
    return render(request, 'personas/personas.html', context)

# Permite Buscar personas por nombre
def buscar_personas(request):
    
    name = request.POST['buscar_persona']
    persona =  models.tb_people.objects.filter(name_people__contains = name)
    context = {'personas':persona}
    
    return render(request, 'personas/personas.html', context)

# Redirije al formulario para agregar personas
def form_persona(request):
    
    org = models.tb_org.objects.all()
    
    return render(request, 'personas/formulario_personas.html', {'orgs':org})

# Agrega una nueva persona a la base de datos
def agregar_persona(request):
    
    name = request.POST['name']
    correo = request.POST['email']
    id_org = request.POST['org']
        
    if id_org != "0":
        org = models.tb_org.objects.get(id_org = id_org)
    else:
        org = models.tb_org.objects.get(org_name = 'Sin organizacion')
        
    persona = models.tb_people(email_people = correo, name_people = name, id_org = org)
    persona.save()        
    
    return redirect("/personas/")

# Envia al formulario para actualizar los datos de una persona
def actualizar_persona(request, id_persona):
    
    persona = models.tb_people.objects.get(email_people = id_persona)
    org = models.tb_org.objects.all()
    org_ = models.tb_org.objects.get(org_name = persona.id_org)
    
    context ={ 'persona' : persona, 'orgs': org , "org_" : org_.id_org}    
    
    return render(request, 'personas/actualizar_persona.html', context)

# Guarda los cambios realizdos en el registro
def update_persona(request, id_persona):
        
    persona = models.tb_people.objects.get(email_people = id_persona)
    
    correo = request.POST['email']
    name = request.POST['name']
    org = request.POST['org']
    
    # En caso de que se desee cambiar el correo
    if persona.email_people != correo:
        # Elimino el registro
        persona.delete()
        # Instancia de la organización
        id_org = models.tb_org.objects.get(id_org = org)
        # Nuevo registro con los datos seleccionados
        persona = models.tb_people(email_people = correo, name_people = name, id_org = id_org )
        persona.save()
        
    # En caso contrario se actualiza org y name
    else:
        id_org = models.tb_org.objects.get(id_org = org)
        persona.id_org = id_org
        persona.name_people = name
        persona.save()
    
    return redirect('/personas/')

# Muestra los permisos relacionados a la persona seleccionada persona
def permisos_persona(request, id_persona):
    
    persona = models.tb_people.objects.get(email_people = id_persona)
    permisos = models.tb_permissions.objects.filter(email_people = id_persona)
    context = {"permisos": permisos, "persona":persona.name_people, "email":id_persona}
   
    return render(request, 'personas/permisos_persona.html', context)

def eliminar_permiso(request, id_persona, id_permiso):
    
    permiso = models.tb_permissions.objects.get(id_permission = id_permiso)
    permiso.delete()

    return redirect('permisos_persona', id_persona)
    
def modificar_permiso(request, id_persona, id_permiso):
    
    orgs = models.tb_org.objects.all()
    sites = models.tb_sites.objects.all()
    zones = models.tb_zones.objects.all()
        
    permiso = models.tb_permissions.objects.get(id_permission = id_permiso)
    
    org_ = models.tb_org.objects.get(org_name = permiso.id_org)
    site_ = models.tb_sites.objects.get(site_name = permiso.id_site)
    zone_ = models.tb_zones.objects.get(zone_name = permiso.id_zone)

    var = permiso.level
    
    context = {"orgs":orgs, "sites":sites, "zones":zones, "permiso":permiso, "org":org_, "site":site_, "zone":zone_, "var":var, "email": id_persona, "id_permiso":id_permiso}
    
    return render(request, 'personas/formulario_actualizar_permiso.html', context)

def guardar_modificar_permiso(request, id_persona, id_permiso):
    
    org     = request.POST.get('org')
    site    = request.POST.get('site')
    zone    = request.POST.get('zone') 
    level   = request.POST.get('permiso')
    
    org_ = models.tb_org.objects.get(id_org = org)
    site_ = models.tb_sites.objects.get(id_site = site)
    zone_ = models.tb_zones.objects.get(id_zone = zone)
    people_ = models.tb_people.objects.get(email_people = id_persona)
    
    permiso = models.tb_permissions(email_people = people_, id_org = org_, id_site = site_, id_zone = zone_, level = level)
    permiso.save()
    
    #print('aca andamos pa', id_persona)
    return redirect('permisos_persona', id_persona)

# Envia al formulario para asignar nuevos permisos a una persona
def formulario_permisos(request, id_persona):
    
    org = models.tb_org.objects.all()
    sites = models.tb_sites.objects.all()
    zones = models.tb_zones.objects.all()
    
    #print(id_persona)
    context = {"org":org, "sites":sites, "zones":zones, "email": id_persona}
    
    return render(request, 'personas/formulario_permisos_persona.html', context)

# Guarda el permiso asignado el id de la persona
def guardar_permiso(request, id_persona):
    
    org     = request.POST.get('org')
    site    = request.POST.get('site')
    zone    = request.POST.get('zone') 
    level   = request.POST.get('permiso')
    
    org_ = models.tb_org.objects.get(id_org = org)
    site_ = models.tb_sites.objects.get(id_site = site)
    zone_ = models.tb_zones.objects.get(id_zone = zone)
    people_ = models.tb_people.objects.get(email_people = id_persona)
    
    permiso = models.tb_permissions(email_people = people_, id_org = org_, id_site = site_, id_zone = zone_, level = level)
    permiso.save()
    
    return redirect('permisos_persona', id_persona)

#---------------------#
#     Dispositivos    #
#---------------------#

# Muestra el template con la lista de dispositivos
def dispositivos(request):
    
    devices = models.tb_devices.objects.select_related('id_cpu', 'id_os', 'id_device_type').all()
    context = {'devices':devices}
    
    return render(request, 'dispositivos/dispositivos.html', context)

def buscar_dispositivos(request):
    
    id_dis = request.POST['dispositivo']
    device = models.tb_devices.objects.select_related('id_cpu', 'id_os', 'id_device_type').filter(ip_from__contains = id_dis)
    context = {'devices':device}
    
    return render(request, 'dispositivos/dispositivos.html', context)

# Muestra el formualario para agregar nuevos dispositivos
def form_dispositivo(request):
    
    # Opciones disponibles en la base de datos para cpus, types, so, y zonas
    cpus = models.tb_cpu.objects.all()
    types = models.tb_device_type.objects.all()
    so    = models.tb_os.objects.all()
    zones = models.tb_zones.objects.all()
    
    context = {"cpus":cpus, "types":types, "os":so, "zones":zones}  
    
    return render(request, 'dispositivos/formulario_dispositivos.html', context)

# Crea la instancia del nuevo dispostivo y la guarda
def agregar_dispositivo(request):
    
    # Toma los valores introducidos en el formulario
    ip = request.POST['ip']
    fecha = request.POST['fecha']
    type = request.POST['type']
    cpu = request.POST['cpu']
    os = request.POST['os']
    zone = request.POST['zone']
    
    # Crea isntancias de las selecciones con llave foranea
    types = models.tb_device_type.objects.get(id_device_type=type)
    cpus = models.tb_cpu.objects.get(id_cpu = cpu)
    so = models.tb_os.objects.get(id_os = os)
    zones = models.tb_zones.objects.get(id_zone = zone)
    
    # Crea una instancia del dispotivo con las opciones seleccionadas y lo guarda
    dispositivo = models.tb_devices(date_created = fecha, id_cpu = cpus, id_os = so, id_device_type = types, ip_from =ip, id_zone = zones)
    dispositivo.save()
    
    return redirect('dispositivos')

# Carga el formulario de actualización con los datos del dispositivo seleccionado
def formulario_actualizar_dispositivo(request, id_device):
    
    # Instancia del equipo seleccionado
    device = models.tb_devices.objects.get(id_device = id_device)
    
    # Instancias de todos los cpu, so, zones, tipos disponibles
    cpus    = models.tb_cpu.objects.all()
    types   = models.tb_device_type.objects.all()
    so      = models.tb_os.objects.all()
    zones   = models.tb_zones.objects.all()
    
    # Instancia de los datos del equipo seleccionado
    cpu_    = models.tb_cpu.objects.get(cpu_name = device.id_cpu)
    so_     = models.tb_os.objects.get(os_name = device.id_os)
    zone_   = models.tb_zones.objects.get(zone_name = device.id_zone)
    device_ = models.tb_device_type.objects.get(id_device_type = str(device.id_device_type))
    
    # Fecha de creación en formato valido para Input Date HTML
    fecha = device.date_created.strftime('%Y-%m-%d')
    
    context = {"device": device, "cpus":cpus, "types":types, "os":so, "zones":zones, "fecha": fecha,
               "so_":so_.id_os, "zone_": zone_.id_zone, "cpu_":cpu_.id_cpu, "device_": device_.id_device_type}
    
    return render(request, 'dispositivos/actualizar_dispositivos.html', context)

# Actualizar la información del dispostivo seleccionado
def actualizar_dispositivo(request, id_device):
    
    # Instancia del dispositivo
    device = models.tb_devices.objects.get(id_device = id_device)
    
    #Asignación d elos nuevos valores
    device.ip_from          = request.POST['ip']
    device.date_created     = request.POST['fecha']
    device.id_device_type   = models.tb_device_type.objects.get(id_device_type = request.POST['type'])
    device.id_cpu           = models.tb_cpu.objects.get(id_cpu = request.POST['cpu'])
    device.id_os            = models.tb_os.objects.get(id_os = request.POST['os'])
    device.id_zone          = models.tb_zones.objects.get(id_zone = request.POST['zone'])
    
    # Guarda los cambios 
    device.save()
        
    return redirect('/dispositivos/') 

# Eliminar dispostivos atravez de la interfaz
def eliminar_dispositivo(request, id_device):
    
    # Instancia del dispositivo seleccionado
    device = models.tb_devices.objects.get(id_device = id_device)
    # Elimina el registro
    device.delete()
    
    return redirect('/dispositivos/')
    
