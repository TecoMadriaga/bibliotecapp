# Generated by Django 4.2.4 on 2023-11-26 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_historialmovimientos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialmovimientos',
            name='descripcion',
        ),
    ]