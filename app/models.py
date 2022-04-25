from django.db import models

# Create your models here.

class student(models.Model):
    s_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique = True)
    rno = models.CharField(max_length=64, unique = True)
    db =  models.BooleanField(default=False)
    # img = models.ImageField(upload_to='NewImages/', default='default.jpg')

# Create your models here.
class Image(models.Model):
 photo = models.ImageField(upload_to="myimage")
 date = models.DateTimeField(auto_now_add=True)
 
class klass(models.Model):
    s_no = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=64, unique = True)
    teacher = models.CharField(max_length=64, unique = True)