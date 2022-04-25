from django.contrib import admin

from app.models import klass, student

# Register your models here.
admin.site.register(student)
admin.site.register(klass)