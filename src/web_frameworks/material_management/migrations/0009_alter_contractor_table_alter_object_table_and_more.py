# Generated by Django 4.0.5 on 2023-02-04 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material_management', '0008_alter_object_name_alter_object_unique_together'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='contractor',
            table='contractor',
        ),
        migrations.AlterModelTable(
            name='object',
            table='object',
        ),
        migrations.AlterModelTable(
            name='requirement',
            table='requirement',
        ),
    ]
