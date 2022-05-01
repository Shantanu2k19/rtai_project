from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #for login
    path('', views.loginPage, name="loginPage"),
    path('handLoginTeacher', views.handLoginTeacher, name="handLoginTeacher"),path('logout',views.handlogout,name="logout"),

    #teacher loggedIn
    path('teacher', views.home, name="teacher"),

    path('updateDB', views.updateDB, name="updateDB"),

    #testing
    path('test',views.test, name="test"),

    #ajax
    path('ajax_test', views.ajax_test, name="ajax_test"),
    path('mark_present', views.mark_present, name="mark_present"),
    path('attendance_for_date', views.attendance_for_date, name="attendance_for_date"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
