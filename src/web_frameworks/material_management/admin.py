from django.contrib import admin
from .models import Requirement, Object, DeliveryQuery, ObjectType, \
    Contractor, MaterialType, DistributionAttribute, \
    RequirementDistributionAttributeValue, DeliveryQueryPosition


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    # exclude = ['slug']
    list_display = [
        'name',
        'unit',
        'contractor',
        'amount',
        'code_string',
        'type',
        'level_4',
        'one_mass',
        'document',
        'object'
    ]
    # ordering = ['-rating']
    list_per_page = 20
    search_fields = ['name']
    list_filter = ['object', 'type', 'unit', 'contractor']
    filter_horizontal = ['distribution_attribute']


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'uuid',
        'type',
        'parent',
    ]
    list_per_page = 10
    search_fields = ['name']
    list_filter = ['type', 'parent', 'name']


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    list_editable = ['name', 'code']
    search_fields = ['name']
    list_per_page = 20


@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']
    search_fields = ['name']
    list_per_page = 20


@admin.register(DistributionAttribute)
class DistributionAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']
    search_fields = ['name']
    list_per_page = 20


@admin.register(RequirementDistributionAttributeValue)
class RequirementDistributionAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['distribution_attribute', 'requirement', 'value']
    list_editable = ['value']
    search_fields = ['distribution_attribute', 'requirement']
    list_per_page = 20


@admin.register(DeliveryQuery)
class DeliveryQueryAdmin(admin.ModelAdmin):
    list_display = [
        'query_number',
        'object',
        'contractor',
        'contract',
        'document',
        'responsible',
    ]
    search_fields = ['object', 'contractor', 'document']
    list_filter = ['object', 'contractor', 'document']
    list_per_page = 20


@admin.register(DeliveryQueryPosition)
class DeliveryQueryPositionAdmin(admin.ModelAdmin):
    list_display = [
        'delivery_query',
        'name',
        'codes_string',
        'amount',
    ]
    list_editable = ['amount']
    search_fields = ['name', 'delivery_query']
    list_per_page = 20
