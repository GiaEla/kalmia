from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Service(models.Model):
    price_no_vat = models.DecimalField('Price without vat', max_digits=9, decimal_places=2, default=0)
    vat = models.DecimalField('Value added tax', max_digits=6, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField('Quantity')
    currency = models.CharField('Currency', max_length=100)


class Invoice(models.Model):
    invoice_number = models.PositiveIntegerField('Invoice', editable=False, null=False)
    place = models.CharField('Place', max_length=100)
    issued = models.DateField('Issued')
    due_date = models.DateField('Due date', null=True, editable=False)
    service_date = models.DateTimeField('Service date')
    reference = models.CharField('Reference', max_length=100)
    services = models.ManyToManyField(Service, through='ServicesQuantity', verbose_name='Services')
    total_no_vat = models.DecimalField('Znesek brez DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    total_with_vat = models.DecimalField('Znesek z DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    payed = models.BooleanField('Plačano', default=False)


class UserProfile(AbstractUser):
    company_name = models.CharField('Company name', max_length=40, blank=True, null=True)
    address = models.CharField('Adress', max_length=50, blank=False, null=False)
    post = models.PositiveIntegerField('Postal code')
    city = models.CharField('City', max_length=40, blank=False, null=False)
    state = models.CharField('State', max_length=40, blank=True, null=True)
    country = models.CharField('Country', max_length=40, blank=True, null=True)
    tax_payer_id = models.CharField('Tax payer id', max_length=40, blank=True, null=True)


class ServicesQuantity(models.Model):
    invoice = models.ForeignKey(Invoice, blank=False, null=False)
    service = models.ForeignKey(Service, blank=False, null=False)
    quantity = models.PositiveIntegerField(default=0)