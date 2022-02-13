from django.db import models


class Location(models.Model):

    LOCATION_TYPE_CHOICES = [
        ('COMP', 'Company'),  # <- for external use
        ('STOR', 'Store'),
        ('WARE', 'Warehouse'),
        ('WEBS', 'Website'),
    ]

    location_type = models.CharField(
        choices=LOCATION_TYPE_CHOICES,
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
        verbose_name_plural = "locations"
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location_type="COMP")


class Company(Location):
    objects = CompanyManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.location_type = "COMP"
        super(Company, self).save(*args, **kwargs)


class StoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location_type="STOR")


class Store(Location):
    objects = StoreManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.location_type = "STOR"
        super(Store, self).save(*args, **kwargs)


class WarehouseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location_type="WARE")


class Warehouse(Location):
    objects = WarehouseManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.location_type = "WARE"
        super(Warehouse, self).save(*args, **kwargs)


class WebsiteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location_type="WEBS")


class Website(Location):
    objects = WebsiteManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.location_type = "WEBS"
        super(Website, self).save(*args, **kwargs)


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


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(person_type="CUST")


class Customer(Person):
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.person_type = "CUST"
        super(Customer, self).save(*args, **kwargs)


class SupplierManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(person_type="SUPP")


class Supplier(Person):
    objects = SupplierManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.person_type = "SUPP"
        super(Supplier, self).save(*args, **kwargs)
