from django.contrib import admin

from app.models import student, Image, record

# Register your models here.
admin.site.register(student)
admin.site.register(Image)
admin.site.register(record)