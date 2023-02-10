from django.db import models


class MaterialType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'material_type'


class Contractor(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.name}, {self.code}'

    class Meta:
        db_table = 'contractor'


class ObjectType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'object_type'


class Object(models.Model):
    uuid = models.UUIDField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ObjectType, on_delete=models.PROTECT)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'{self.type}: {self.name}'

    class Meta:
        unique_together = ['name', 'type']
        db_table = 'object'


class DistributionAttribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'distribution_attribute'


class Requirement(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255, default='')
    unit = models.CharField(max_length=10, blank=True, default='')
    type = models.ForeignKey(MaterialType, on_delete=models.PROTECT, null=True)
    level_3 = models.CharField(max_length=255, blank=True, default='')
    level_4 = models.CharField(max_length=255, blank=True, default='')
    one_mass = models.FloatField(null=True, blank=True)
    amount = models.FloatField()
    code_string = models.CharField(max_length=1000, blank=True, default='')
    document = models.CharField(max_length=255, blank=True, default='')
    document_id = models.CharField(max_length=36, blank=True, default='')
    object = models.ForeignKey(Object, on_delete=models.PROTECT, null=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, null=True, blank=True)
    distribution_attribute = models.ManyToManyField(
        DistributionAttribute,
        through='RequirementDistributionAttributeValue'
    )
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(auto_now=True, editable=False)
    # available = models.FloatField(null=True, blank=True)
    # free_available = models.FloatField(null=True, blank=True)
    # rest_available = models.FloatField(null=True, blank=True)
    # shipped_available = models.FloatField(null=True, blank=True)
    # moving = models.FloatField(null=True, blank=True)
    # delivered = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name[:40] if len(str(self.name)) > 41 else self.name

    class Meta:
        db_table = 'requirement'


class RequirementDistributionAttributeValue(models.Model):
    distribution_attribute = models.ForeignKey(DistributionAttribute, on_delete=models.PROTECT)
    value = models.FloatField(null=True)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['distribution_attribute', 'requirement']
        db_table = 'requirement_distribution_attribute_value'


class DeliveryQuery(models.Model):
    uuid = models.UUIDField(unique=True, blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.PROTECT)
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT)
    query_number = models.CharField(max_length=255)
    contract = models.CharField(max_length=255, blank=True, default='')
    document = models.CharField(max_length=255, blank=True, default='')
    document_id = models.CharField(max_length=36, blank=True, default='')
    responsible = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=255, blank=True, default='')
    permit = models.CharField(max_length=255, blank=True, default='')
    responsible_email = models.CharField(max_length=255, blank=True, default='')
    # author = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='delivery_queries')
    author = models.CharField(max_length=255, blank=True, default='')
    superviser_email = models.CharField(max_length=255, blank=True, default='')
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.query_number}, {self.contractor}'

    class Meta:
        db_table = 'delivery_query'


class DeliveryQueryPosition(models.Model):
    uuid = models.UUIDField(unique=True, blank=True, null=True)
    delivery_query = models.ForeignKey(DeliveryQuery, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    codes_string = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.delivery_query}, {self.name[:40] if len(str(self.name)) > 41 else self.name}'

    class Meta:
        db_table = 'delivery_query_position'
