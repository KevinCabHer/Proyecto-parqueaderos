import re
from sys import orig_argv
from django.shortcuts import render, HttpResponse, redirect
from . import models

# Template Inicio
def inicio(request):
    
    organizaciones = models.tb_org.objects.all().values_list(named=True)
    #print(organizaciones)
    context = {
        "organizaciones": organizaciones,
    }
    
    return render(request, 'organizaciones/organizaciones.html', context)

def tabs_organizacion(request, id_org):
    
    organizaciones = models.tb_org.objects.filter(id_org = id_org).values_list(named = True)
    personas = models.tb_people.objects.filter(id_org = id_org).values_list(named = True)
    zonas = models.tb_zones.objects.filter(id_org = id_org).values()
    
    # ID de los sitios relacionados a las zonas
    # ID de las zonas
    id_sites = []
    id_zonas = []
    for zona in zonas:
        if zona.get('id_site_id') not in id_sites: 
            id_sites.append(zona.get('id_site_id'))
        if zona.get('id_zone') not in id_zonas:
            id_zonas.append(zona.get('id_zone'))
    # información de los sitios relacionados
    sites = {}
    for id_site in id_sites:
        sitio = models.tb_sites.objects.filter(id_site = id_site).values()
        sites[id_site] = sitio
    # Informacion de los equipos realcionados
    devices = {}
   
    for id_zona in id_zonas:
        device = models.tb_devices.objects.select_related('id_cpu', 'id_os', 'id_device_type').filter(id_zone = id_zona)
        
        for dev in device:
            
            devices[dev.id_device] = dev
    
    context = {
        "org": organizaciones,
        "people": personas,
        "zonas": zonas,
        "sites": sites,
        "devices": devices
    }
    
    return render(request, 'organizaciones/tabs_organizacion.html', context)

def agregar_organizacion(request):
    context = {
        
    }
    return render(request, 'organizaciones/formulario_organizaciones.html', context)

# Template Registro de organizaciones
def register_org(request):
    return render(request, 'create/create_org.html', {})

# Agregar nuevas organizaciones
def new_org(request):
    
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
    
    return render(request, 'create/create_org.html', {})

# Template Registro Empleados
def register_employed(request):  
    org = models.tb_org.objects.all()
    context = {
        "organizaciones" : org
    }
    return render(request, 'create/create_employed.html', context)

# Agregar nuevo empleado
def new_employed(request):
    
    # Datos del formulario empleados
    email       = request.POST['email']
    nombre      = request.POST['nombre']
    organizacion = request.POST['organizacion']
    
    # Instancia de la organización seleccionada
    org = models.tb_org.objects.get(id_org = organizacion)
    
    # Instancia de la tabla people con los datos de la nueva persona
    employed = models.tb_people(email_people = email, name_people = nombre, id_org = org )
    employed.save()
    
    org = models.tb_org.objects.all()
    context = {
        "organizaciones" : org
    }
    
    return render(request, 'create/create_employed.html', context)

# Template Registro de equipos
def register_device(request):
    
    # Busqueda de los diferentes elementos para listarlo en los select de los formularios
    type_devices = models.tb_device_type.objects.all()
    cpus = models.tb_cpu.objects.all()
    so = models.tb_os.objects.all()
    zones = models.tb_zones.objects.all()
    
    context = {
        "type_devices" : type_devices,
        "cpus" : cpus,
        "so"   : so,
        "zones": zones
        } 
    
    return render(request, 'create/create_device.html', context)

# Agregar nuevo equipo
def new_device(request):
    
    # Datos del formulario nuevo equipo
    ip = request.POST['ip']
    type = request.POST['tipo_equipo']
    cpu = request.POST['procesador']
    so = request.POST['so']
    date = request.POST['fecha']
    zone = request.POST['zone_']
    
    # Consulta de las llaves foraneas
    cpu = models.tb_cpu.objects.get(id_cpu = cpu)
    os = models.tb_os.objects.get(id_os = so)
    type_device = models.tb_device_type.objects.get(id_device_type = type)
    zone = models.tb_zones.objects.get(id_zone = zone)
    
    # Instancia de la tabla tb_devices con los datos del nuevo equipo
    device = models.tb_devices(id_cpu = cpu, id_os = os, id_device_type = type_device, ip_from = ip, date_created = date, id_zone = zone)
    device.save()
    
    # Busqueda de los diferentes elementos para listarlo en los select de los formularios
    type_devices = models.tb_device_type.objects.all()
    cpus = models.tb_cpu.objects.all()
    so = models.tb_os.objects.all()
    zones = models.tb_zones.objects.all()
    
    context = {
        "type_devices" : type_devices,
        "cpus" : cpus,
        "so"   : so,
        "zones": zones
        } 
    
    return render(request, 'create/create_device.html', context)

# Template registro zonas
def register_zone(request):
    
    # Busqueda de los diferentes elementos para listarlo en los select de los formularios
    sites = models.tb_sites.objects.all()
    org = models.tb_org.objects.all()
    context = {
        'sites':sites,
        'orgs':org
               }
    
    return render(request, 'create/create_zone.html', context)

def new_zone(request):
    # Instancia de la organización y sitio seleccinado
    org = models.tb_org.objects.get(id_org = request.POST['org'])
    site = models.tb_sites.objects.get(id_site = request.POST['site'])
    # Instancia del modelo con los datos del nuevo registro
    zone = models.tb_zones(zone_name=request.POST['name'], id_org=org, id_site=site)
    zone.save()
    
    # Busqueda de los diferentes elementos para listarlo en los select de los formularios
    sites = models.tb_sites.objects.all()
    org = models.tb_org.objects.all()
    context = {
        'sites':sites,
        'orgs':org
               }
    
    return render(request, 'create/create_zone.html', context)

# Mostrar elementos 
def consulta(request):
    
    # Varaibles de control para condicionar lo que se muestra en el template
    org_ = 0
    employed_ = 0
    devices_ = 0
    
    # Elementos encontrados en las diferentes listas
    org      = models.tb_org.objects.all()
    employed = models.tb_people.objects.all()
    devices  = models.tb_devices.objects.all()
   
   # Comprueba si hay registros existentes
    if org.exists():
        org_ = 1
    if employed.exists():
        employed_ = 1
    if devices.exists():
        devices_ = 1
    
    context = {
        "organizaciones" : org,
        "empleados" : employed,
        "equipos" : devices, 
        "org_" : org_,
        "employed" : employed_,
        "dev" : devices_,
    }
    
    
    return render(request, 'read_update_delete/rud.html', context)

# Eliminar Organizaciones
def delete_org(request, id_org):
    
    org = models.tb_org.objects.get(id_org = id_org)
    org.delete()
    
    return redirect('/consulta/')    

# Eliminar empleados
def delete_employed(request, id_people):
    
    employed = models.tb_people.objects.get(id_people = id_people)
    employed.delete()
    
    return redirect('/consulta/')

# Eliminar equipos
def delete_device(request, id_device):
    
    devices = models.tb_devices.objects.get(id_device = id_device)
    devices.delete()
    
    return redirect('/consulta/')

# Muestra el formulario de organizacion corespondiente para ser actualizado
def update_org(request, id_org):
    
    # Objeto con los datos seleccionadas    
    org = models.tb_org.objects.get(id_org = id_org)
    context = {'org' : org}
    return render(request, 'read_update_delete/update_org.html', context)

# Actualiza los datos de la organización
def u_org(request, id_org):
    
    # Objeto con la organización seleccionada
    org = models.tb_org.objects.get(id_org = id_org)
     
    # Datos del formulario Organización asignados al objeto
    org.org_name    = request.POST['name']
    org.org_tax_id  = request.POST['id_tag']
    org.country     = request.POST['country']
    org.city        = request.POST['city']
    org.addres      = request.POST['address']
    org.postal      = request.POST['postal']
    
    # Guarda el objeto con los nuevos valores
    org.save()
    
    return redirect('/consulta/')

# Muestra el template de actualización del empleado elegido con los datos correspondientes
def update_emp(request, id_emp):
    
    empl = models.tb_people.objects.get(id_people = id_emp)
    context = {'empl' : empl}
    return render(request, 'read_update_delete/update_employed.html', context)

# Guarda los cambios realizados en el formulario correspondiente al empleado
def u_emp(request, id_emp):
    
    empl = models.tb_people.objects.get(id_people = id_emp)
    empl.email_people = request.POST['email']
    empl.name_people = request.POST['nombre']
    org = request.POST['organizacion']
    
    # En caso de seleccionar una organización se actualiza, en caso contrario no se altera el campo
    if org != "default":
        empl.id_org = models.tb_org.objects.get(id_org = org)
     
    empl.save()
    return redirect('/consulta/')
  

def update_dev(request, id_dev):
    
    type_devices = models.tb_device_type.objects.all()
    cpus = models.tb_cpu.objects.all()
    so = models.tb_os.objects.all()
    zones = models.tb_zones.objects.all()
    
    dev = models.tb_devices.objects.select_related('id_device_type').get(id_device = id_dev)
    
    cpu_ = models.tb_cpu.objects.get(cpu_name = dev.id_cpu)
    so_ = models.tb_os.objects.get(os_name = dev.id_os)
    zone_ = models.tb_zones.objects.get(zone_name = dev.id_zone)
    print(dev.id_zone)
    
    context = {
        "type_devices" : type_devices,
        "cpus" : cpus,
        "so"   : so,
        "zones": zones,
        "dev"  : dev,
        "cpu_" : cpu_.id_cpu,
        "so_"  : so_.id_os,
        "zone_": zone_.zone_name,
        "select_type": dev.id_device_type.type_name,
        }
    
    return render(request, 'read_update_delete/update_device.html', context)

def u_dev(request, id_dev):
    
    return HttpResponse("ahi fue")
