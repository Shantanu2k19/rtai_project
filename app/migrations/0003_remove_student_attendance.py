# Generated by Django 4.0.4 on 2022-04-28 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_images_title_remove_images_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='attendance',
        ),
    ]
