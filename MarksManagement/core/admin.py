from django.contrib import admin
from .models import User, Subject, Student, Marks

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Marks)
