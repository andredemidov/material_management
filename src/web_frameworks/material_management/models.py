from django.db import models


class MaterialType(models.Model):
    name = models.CharField(max_length=255)


class Contractor(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)


class ObjectType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Object(models.Model):
    uuid = models.UUIDField(unique=True)
    type = models.ForeignKey(ObjectType, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)


class Requirement(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)
    type = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, null=True)
    level_3 = models.CharField(max_length=255, blank=True, null=True)
    level_4 = models.CharField(max_length=255, blank=True, null=True)
    one_mass = models.FloatField(null=True, blank=True)
    amount = models.FloatField()
    code_string = models.CharField(max_length=1000, blank=True, null=True)
    document = models.CharField(max_length=255, blank=True, null=True)
    document_id = models.CharField(max_length=36, blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True)
    available = models.FloatField(null=True, blank=True)
    free_available = models.FloatField(null=True, blank=True)
    rest_available = models.FloatField(null=True, blank=True)
    shipped_available = models.FloatField(null=True, blank=True)
    moving = models.FloatField(null=True, blank=True)
    delivered = models.FloatField(null=True, blank=True)


class DeliveryQuery(models.Model):
    uuid = models.UUIDField(unique=True, blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True)
    query_number = models.CharField(max_length=255, blank=True, null=True)
    contract = models.CharField(max_length=255, blank=True, null=True)
    document = models.CharField(max_length=255, blank=True, null=True)
    document_id = models.CharField(max_length=36, blank=True, null=True)
    responsible = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    permit = models.CharField(max_length=255, blank=True, null=True)
    responsible_email = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    superviser_email = models.CharField(max_length=255, blank=True, null=True)


class DeliveryQueryPosition(models.Model):
    uuid = models.UUIDField(unique=True, blank=True, null=True)
    delivery_query = models.ForeignKey(DeliveryQuery, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    codes_string = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField()
