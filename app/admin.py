from django.contrib import admin

from app.models import klass, student, Image

# Register your models here.
admin.site.register(student)
admin.site.register(klass)
admin.site.register(Image)