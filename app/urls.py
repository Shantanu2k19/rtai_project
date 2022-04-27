from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('teacher', views.home, name="teacher"),

    #for login
    path('', views.loginPage, name="loginPage"),
    path('handLoginTeacher', views.handLoginTeacher, name="handLoginTeacher"),

    path('test',views.test, name="test"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
