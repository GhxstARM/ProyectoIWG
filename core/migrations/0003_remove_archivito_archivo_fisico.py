# Generated by Django 4.2.7 on 2023-12-05 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_archivito_archivo_fisico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivito',
            name='archivo_fisico',
        ),
    ]
