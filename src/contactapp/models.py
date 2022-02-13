from django.db import models


class Company(models.Model):

    COMPANY_TYPE_CHOICES = [
        ('BLOG', 'Blog'),
        ('LOCA', 'Location'),
        ('SUPP', 'Suppplier'),
        ('CUST', 'Customer'),
    ]

    company_type = models.CharField(
        choices=COMPANY_TYPE_CHOICES,
        max_length=4, blank=True)
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    domain = models.CharField(
            'Domain eg. example.com',
            max_length=200,
            blank=True)
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
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class LocationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(company_type="LOCA")


class Location(Company):
    objects = LocationManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.company_type = "LOCA"
        super(Supplier, self).save(*args, **kwargs)


class SupplierManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(company_type="SUPP")


class Supplier(Company):
    objects = SupplierManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.company_type = "SUPP"
        super(Supplier, self).save(*args, **kwargs)


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
        choices=PERSON_TYPE_CHOICES,
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
