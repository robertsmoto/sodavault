from django.db import models
import configapp.models


class LocationCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='LOCACAT')


class LocationCategory(configapp.models.Group):

    objects = LocationCategoryManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.group_type = 'LOCACAT'
        super(LocationCategory, self).save(*args, **kwargs)


class LocationTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='LOCATAG')


class LocationTag(configapp.models.Group):

    objects = LocationTagManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.group_type = 'LOCATAG'
        super(LocationTag, self).save(*args, **kwargs)


class Location(models.Model):

    LOCATION_TYPE_CHOICES = [
        ('COMP', 'Company'),  # <- for external use
        ('SUPP', 'Supplier'),  # <- for external use
        ('STOR', 'Store'),
        ('WARE', 'Warehouse'),
        ('WEBS', 'Website'),
    ]
    categories = models.ManyToManyField(
            LocationCategory,
            related_name="category_locations",
            blank=True)
    tags = models.ManyToManyField(
            LocationTag,
            related_name="tag_locations",
            blank=True)
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

    class Meta:
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
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.location_type = "COMP"
        super(Company, self).save(*args, **kwargs)


class SupplierManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(location_type="SUPP")


class Supplier(Location):
    objects = SupplierManager()

    class Meta:
        proxy = True
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.location_type = "SUPP"
        super(Supplier, self).save(*args, **kwargs)


class StoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location_type="STOR")


class Store(Location):
    objects = StoreManager()

    class Meta:
        proxy = True
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ['name']

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
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.location_type = "WARE"
        super(Warehouse, self).save(*args, **kwargs)




class PersonCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='PERSCAT')


class PersonCategory(configapp.models.Group):
    objects = PersonCategoryManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.group_type = 'PERSCAT'
        super(PersonCategory, self).save(*args, **kwargs)


class PersonTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='PERSTAG')


class PersonTag(configapp.models.Group):

    objects = PersonTagManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.group_type = 'PERSTAG'
        super(PersonTag, self).save(*args, **kwargs)


class Person(models.Model):

    companies = models.ManyToManyField(
            Location,
            related_name='company_people',
            blank=True)
    suppliers = models.ManyToManyField(
            Location,
            related_name='supplier_people',
            blank=True)
    stores = models.ManyToManyField(
            Location,
            related_name='store_people',
            blank=True)
    warehouses = models.ManyToManyField(
            Location,
            related_name='warehouse_people',
            blank=True)
    websites = models.ManyToManyField(
            Location,
            related_name='website_people',
            blank=True)
    categories = models.ManyToManyField(
            PersonCategory,
            related_name="category_people",
            blank=True)
    tags = models.ManyToManyField(
            PersonTag,
            related_name="tag_people",
            blank=True)
    PERSON_TYPE_CHOICES = [
        ('CUST', 'Customer'),
        ('CONT', 'Contact'),
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
    ship_zipcode = models.CharField(max_length=200, blank=True)

    class Meta():
        verbose_name_plural = "People"

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(person_type="CUST")


class Customer(Person):
    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['lastname', 'firstname']

    def save(self, *args, **kwargs):
        self.person_type = "CUST"
        super(Customer, self).save(*args, **kwargs)


class ContactManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(person_type="CONT")


class Contact(Person):
    objects = ContactManager()

    class Meta:
        proxy = True
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['lastname', 'firstname']

    def save(self, *args, **kwargs):
        self.person_type = "CONT"
        super(Contact, self).save(*args, **kwargs)
