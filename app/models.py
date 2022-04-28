from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from sqlalchemy import false

# Create your models here.
class images(models.Model):
    im_no = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to="myimage")
    date = models.DateTimeField(auto_now_add=True)

class student(models.Model):
    s_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    rno = models.CharField(max_length=64, unique = True)
    db =  models.BooleanField(default=False)
    img = models.ForeignKey(images, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return f"{self.s_no} : {self.name}({self.rno})" 

class record(models.Model):
    datee = models.CharField(primary_key=True,max_length=64)
    presentStudents =  models.CharField(max_length=128, null=True)

    def __str__(self):
        return f"{self.datee} : {self.presentStudents}" 