from django.db import models

class Service(models.Model):
    service_titie=models.CharField(max_length=30)
    service_dis=models.CharField(max_length=50)
    service_field=models.CharField(max_length=40)

    
    
# Create your models here.
