# Generated by Django 3.1.2 on 2022-04-25 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_student_db'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='img',
            field=models.ImageField(default='default.jpg', upload_to='images/'),
        ),
    ]
