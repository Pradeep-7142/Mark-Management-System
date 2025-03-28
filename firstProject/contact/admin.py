from django.contrib import admin
from contact.models import Contact

class contactAdmin(admin.ModelAdmin):
    list_display=('name','email','phone','message')

admin.site.register(Contact,contactAdmin)
# Register your models here.
