# Generated by Django 4.2.4 on 2023-11-24 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_libro_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='descripcion',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
