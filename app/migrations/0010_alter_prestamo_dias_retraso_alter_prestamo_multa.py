# Generated by Django 4.2.4 on 2023-11-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_prestamo_costo_prestamo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='dias_retraso',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='multa',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, null=True),
        ),
    ]
