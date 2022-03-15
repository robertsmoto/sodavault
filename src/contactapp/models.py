from django.db import models
import configapp.models


class Category(configapp.models.GroupABC):
    class Meta(configapp.models.GroupABC.Meta):
        verbose_name_plural = '__ categories'


class Tag(configapp.models.GroupABC):
    class Meta(configapp.models.GroupABC.Meta):
        verbose_name_plural = '__ tags'


class Location(models.Model):
    categories = models.ManyToManyField(
            Category,
            blank=True)
    tags = models.ManyToManyField(
            Tag,
            blank=True)
    LOCATION_TYPE_CHOICES = [
            ('COMP', 'Company'),
            ('STOR', 'Store'),
            ('SUPP', 'Supplier'),
            ('WARE', 'Warehouse'),
            ('WEBS', 'Website'),
            ]
    location_type = models.CharField(
            max_length=4,
            choices=LOCATION_TYPE_CHOICES,
            blank=True)
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

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class CompanyManager(models.Manager):

    def get_queryset(self):
        return super(CompanyManager, self).get_queryset().filter(
                location_type="COMP")


class Company(Location):
    objects = CompanyManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.location_type = "COMP"
        return super().save(**kwargs)


class StoreManager(models.Manager):

    def get_queryset(self):
        return super(StoreManager, self).get_queryset().filter(
                location_type="STOR")


class Store(Location):
    objects = StoreManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.location_type = "STOR"
        return super().save(**kwargs)


class SupplierManager(models.Manager):

    def get_queryset(self):
        return super(SupplierManager, self).get_queryset().filter(
                location_type="SUPP")


class Supplier(Location):
    objects = SupplierManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.location_type = "SUPP"
        return super().save(**kwargs)


class WarehouseManager(models.Manager):

    def get_queryset(self):
        return super(WarehouseManager, self).get_queryset().filter(
                location_type="WARE")


class Warehouse(Location):
    objects = WarehouseManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.location_type = "WARE"
        return super().save(**kwargs)


class WebsiteManager(models.Manager):

    def get_queryset(self):
        return super(WebsiteManager, self).get_queryset().filter(
                location_type="WEBS")


class Website(Location):
    objects = WebsiteManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.location_type = "WEBS"
        return super().save(**kwargs)


class Person(models.Model):
    locations = models.ManyToManyField(
            Location,
            blank=True)
    categories = models.ManyToManyField(
            Category,
            blank=True)
    tags = models.ManyToManyField(
            Tag,
            blank=True)
    PERSON_TYPE_CHOICES = [
            ('CUST', 'Customer'),
            ('CONT', 'Contact'),
            ]
    person_type = models.CharField(
            max_length=4,
            choices=PERSON_TYPE_CHOICES,
            blank=True
            )
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
    ship_zipcode = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


class ContactManager(models.Manager):

    def get_queryset(self):
        return super(ContactManager, self).get_queryset().filter(
                person_type="CONT")


class Contact(Person):
    objects = ContactManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.person_type = "CONT"
        return super().save(**kwargs)


class CustomerManager(models.Manager):

    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(
                person_type="CUST")


class Customer(Person):
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.person_type = "CUST"
        return super().save(**kwargs)


