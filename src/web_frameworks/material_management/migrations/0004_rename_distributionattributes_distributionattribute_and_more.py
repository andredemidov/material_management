# Generated by Django 4.0.5 on 2023-02-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_management', '0003_alter_deliveryquery_table_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DistributionAttributes',
            new_name='DistributionAttribute',
        ),
        migrations.AddField(
            model_name='requirement',
            name='distribution_attribute',
            field=models.ManyToManyField(through='material_management.RequirementDistributionAttributeValue', to='material_management.distributionattribute'),
        ),
    ]
