from django.db import models

# Create your models here.
class Image(models.Model):
    im_no = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to="myimage")
    date = models.DateTimeField(auto_now_add=True)

class student(models.Model):
    s_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    rno = models.CharField(max_length=64, unique = True)
    db =  models.BooleanField(default=False)
    img = models.ForeignKey(Image, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.s_no} : {self.name}({self.rno})" 

class klass(models.Model):
    s_no = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=64)
    teacher = models.CharField(max_length=64)