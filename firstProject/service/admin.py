from django.contrib import admin
from service.models import Service

class ServiceAdmin(admin.ModelAdmin):
    list_display=('service_titie','service_dis','service_field')

admin.site.register(Service,ServiceAdmin)
# Register your models here.
