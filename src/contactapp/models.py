from django.db import models

# Create your models here.
class Company(models.Model):

    COMPANY_TYPE_CHOICES = [ 
        ('BLOG', 'Blog'), 
        ('LOCA', 'Location'), 
        ('SUPP', 'Suppplier'), 
        ('CUST', 'Customer'),
    ]
    company_type = models.CharField(
        choices = COMPANY_TYPE_CHOICES,
        max_length=4, blank=True)
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    address_01 = models.CharField(max_length=200, blank=True)
    address_02 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    ship_address_01 = models.CharField(max_length=200, blank=True)
    ship_address_02 = models.CharField(max_length=200, blank=True)
    ship_city = models.CharField(max_length=200, blank=True)
    ship_state = models.CharField(max_length=200, blank=True)
    ship_zipcode = models.CharField(max_length=200, blank=True)

    class Meta():
        verbose_name_plural = "companies"

    def __str__(self):
        return '{}'.format(self.name)

"""
Think about using expanded location mangers:
    1. ecommerce
    2. warehouse
    3. retail
"""

class LocationManager(models.Manager):
    def get_queryset(self):
        return super(LocationManager, self).get_queryset().filter(
            company_type='LOCA').order_by('name')

    def create(self, **kwargs):
        kwargs.update({'company_type': 'LOCA'})
        return super(LocationManager, self).create(**kwargs)

class Location(Company):
    objects = LocationManager()
    class Meta:
        proxy = True

class SupplierManager(models.Manager):
    def get_queryset(self):
        return super(SupplierManager, self).get_queryset().filter(
            company_type='SUPP').order_by('name')

    def create(self, **kwargs):
        kwargs.update({'company_type': 'SUPP'})
        return super(SupplierManager, self).create(**kwargs)

class Supplier(Company):
    objects = SupplierManager()
    class Meta:
        proxy = True

class Person(models.Model):
    company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    PERSON_TYPE_CHOICES = [ 
        ('CUST', 'Customer'),
        ('SUPP', 'Suppplier'), 
    ]
    person_type = models.CharField(
        choices = PERSON_TYPE_CHOICES,
        max_length=4, blank=True)
    firstname = models.CharField(max_length=200, blank=True)
    lastname = models.CharField(max_length=200, blank=True)
    nickname = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    address_01 = models.CharField(max_length=200, blank=True)
    address_02 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    ship_address_01 = models.CharField(max_length=200, blank=True)
    ship_address_02 = models.CharField(max_length=200, blank=True)
    ship_city = models.CharField(max_length=200, blank=True)
    ship_state = models.CharField(max_length=200, blank=True)
    shop_zipcode = models.CharField(max_length=200, blank=True)

    class Meta():
        verbose_name_plural = "people"

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


