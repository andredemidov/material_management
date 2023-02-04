# Generated by Django 4.0.5 on 2023-02-04 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material_management', '0006_alter_object_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryquery',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default='2000-1-1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deliveryquery',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='deliveryqueryposition',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default='2000-1-1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deliveryqueryposition',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='requirement',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default='2000-1-1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirement',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='author',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='contract',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material_management.contractor'),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='document',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='document_id',
            field=models.CharField(blank=True, default='', max_length=36),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material_management.object'),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='permit',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='query_number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='responsible',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='responsible_email',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='deliveryquery',
            name='superviser_email',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='object',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='material_management.object'),
        ),
        migrations.AlterField(
            model_name='object',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material_management.objecttype'),
        ),
        migrations.AlterField(
            model_name='object',
            name='uuid',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='code_string',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='contractor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='material_management.contractor'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='document',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='document_id',
            field=models.CharField(blank=True, default='', max_length=36),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='level_3',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='level_4',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='material_management.object'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='material_management.materialtype'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='unit',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='requirementdistributionattributevalue',
            name='distribution_attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material_management.distributionattribute'),
        ),
        migrations.AlterField(
            model_name='requirementdistributionattributevalue',
            name='requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material_management.requirement'),
        ),
    ]
