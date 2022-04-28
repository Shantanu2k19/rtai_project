from django.contrib import admin

from app.models import student, images, record

# Register your models here.
admin.site.register(student)
admin.site.register(images)
admin.site.register(record)