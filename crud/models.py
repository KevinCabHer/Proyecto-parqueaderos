from re import T
from socket import INADDR_ALLHOSTS_GROUP
from django.db import models
   
# Tabla de organizaciones   
class tb_org(models.Model): 
    
    id_org      = models.AutoField(db_column='IdOrg', primary_key=True)
    org_name    = models.CharField(db_column='OrgName', max_length=100, blank=True, null=True)
    org_tax_id  = models.CharField(db_column='OrgTaxID', max_length=50, blank=True, null=True)
    country     = models.CharField(db_column='Country', max_length=20, blank=True, null=True)
    city        = models.CharField(db_column='City', max_length=100, blank=True, null=True)
    addres      = models.CharField(db_column='Address', max_length=100, blank=True, null=True)
    postal      = models.CharField(db_column='Postal', max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.org_name
    
    class Meta:
        managed = True
        db_table = 'Tb_Org'
        
# Tabla de sitios 
class tb_sites(models.Model):
    
    id_site    = models.AutoField(db_column='IdSite', primary_key=True) 
    site_name  = models.CharField(db_column='SiteName', max_length=100, blank=True, null=True)
    country    = models.CharField(db_column='Country', max_length=20, blank=True, null=True)
    city       = models.CharField(db_column='City', max_length=100, blank=True, null=True)
    address    = models.CharField(db_column='Address', max_length=100, blank=True, null=True)
    postal     = models.CharField(db_column='Postal', max_length=15, blank=True, null=True)
    id_org     = models.ManyToManyField(tb_org)
    
    def __str__(self):
        return self.site_name

    class Meta:
        managed = True
        db_table = 'Tb_Sites'

                      
# Tabla de Zonas
class tb_zones(models.Model):
    
    id_zone    = models.AutoField(db_column='IdZone', primary_key=True) 
    zone_name  = models.CharField(db_column='ZoneName', max_length=100, blank=True, null=True)  
    id_site    = models.ForeignKey('tb_sites', on_delete=models.PROTECT, db_column='IdSite') 
    # on_delete=models.PROTECT -> Prohibe eliminar la informacion de los datos referenciados (organizaciones, sitios)
    # Hasta que no se eliminen todas las zonas relacionadas
    
    def __str__(self):
        return self.zone_name

    class Meta:
        
        managed = True
        db_table = 'Tb_Zones'
        

# Tabla de Equipos   
class tb_devices(models.Model):
                    
    id_device       = models.BigAutoField(db_column='IdDevice', primary_key=True)
    date_created    = models.DateTimeField(db_column='DateCreated') 
    id_cpu          = models.ForeignKey('tb_cpu', on_delete=models.PROTECT, db_column='IdCpu') 
    id_os           = models.ForeignKey('tb_os', on_delete=models.PROTECT, db_column='IdOS')   
    id_device_type  = models.ForeignKey('tb_device_type', on_delete=models.PROTECT, db_column='IdDeviceType')
    ip_from         = models.CharField(db_column='IpFrom', max_length=100, blank=True, null=True)
    
    id_zone         = models.ForeignKey('tb_zones', on_delete=models.PROTECT, db_column='IdZone') 
    # on_delete=models.PROTECT -> Prohibe la eliminacion de los equipos en caso de eliminarse los elementos de las tablas
    # realcionadas con foreng key
    
    def __str__(self):
        return self.ip_from

    class Meta:
        managed = True
        db_table = 'Tb_Devices'

# Tabla información cpu       
class tb_cpu(models.Model):
    
    id_cpu      = models.AutoField(db_column='IdCpu', primary_key=True) 
    cpu_name    = models.CharField(db_column='CpuName',max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.cpu_name

    class Meta:
        managed = True
        db_table = 'Tb_CPU'

# Tabla descripción sistema operativo
class tb_os(models.Model):
    
    id_os   = models.AutoField(db_column='IdOS', primary_key=True) 
    os_name = models.CharField(db_column='OsName',max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.os_name

    class Meta:
        managed = True
        db_table = 'Tb_OS'

# Tabla tipo de equipo      
class tb_device_type (models.Model):
    
    id_device_type   = models.AutoField(db_column='IdDeviceType', primary_key=True) 
    type_name        = models.CharField(db_column='TypeName',max_length=100, blank=True, null=False)
    type_description = models.CharField(db_column="TypeDescription", max_length=200, null=False)
    
    def __str__(self):
        return str(self.id_device_type)

    class Meta:
        managed = True
        db_table = 'Tb_Device_Type'
    
# Tabla-> relaciona devices con zonas. sitios y organizaciones (?)   
class tb_provisioning(models.Model):
    id_provisioning = models.AutoField(db_column='Id', primary_key=True)
    id_org      = models.IntegerField(db_column='IdOrg', blank=True, null=True) 
    id_site     = models.IntegerField(db_column='IdSite', blank=True, null=True) 
    id_zone     = models.IntegerField(db_column='IdZone', blank=True, null=True) 
    id_device   = models.IntegerField(db_column='IdDevice', blank=True, null=True) 
    description = models.CharField(db_column="Description", max_length=100, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'Tb_provisioning'
        
# Tabla personas
class tb_people(models.Model):
    
    email_people    = models.EmailField(db_column='EmailPeople', max_length=200, primary_key=True)
    name_people     = models.CharField(db_column='NamePeople',max_length=100, blank=True, null=True)
    id_org          = models.ForeignKey('tb_org', on_delete=models.PROTECT, db_column='IdOrg')
    # on_delete=models.PROTECT
    # No permite la eliminación de las personas relacionadas con un organización, en caso de que
    # esta ultima sea eliminada
    
    def __str__(self):
        return self.name_people

    class Meta:
        managed = True
        db_table = 'Tb_People'
        
# Tabla permisos personas
class tb_permissions(models.Model):
    id_permission   = models.AutoField(db_column='IdPermission', primary_key=True)
    email_people    = models.ForeignKey('tb_people', on_delete=models.CASCADE, db_column='EmailPeople')
    id_org          = models.IntegerField(db_column='IdOrg', blank=True, null=True)
    id_site         = models.IntegerField(db_column='IdSite', blank=True, null=True)    
    id_zone         = models.IntegerField(db_column='IdZone', blank=True, null=True) 
    id_device       = models.IntegerField(db_column='IdDevice', blank=True, null=True) 
    
    class Meta:
        managed = True
        db_table = 'Tb_Permissions'