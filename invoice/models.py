from __future__ import unicode_literals

from _decimal import Decimal
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models

from invoice.generators import create_pdf


class Vat(models.Model):
    name = models.CharField('Value added tax', max_length=40, blank=True, null=True)
    value = models.DecimalField('Vat value', max_digits=8, decimal_places=2, default=0, editable=False)


class Service(models.Model):
    name = models.CharField('Service', max_length=40, blank=True, null=True)
    price_no_vat = models.DecimalField('Price without vat', max_digits=9, decimal_places=2, default=0)
    vat = JSONField('Vat', default=None)
    quantity = models.PositiveIntegerField('Quantity', default=0)
    currency = models.CharField('Currency', max_length=100)


class Customer(models.Model):
    name = models.CharField('Name', max_length=40, blank=True, null=True)
    last_name = models.CharField('Last name', max_length=40, blank=True, null=True)
    company_name = models.CharField('Company name', max_length=40, blank=True, null=True)
    address = models.CharField('Adress', max_length=50, blank=True, null=True)
    post = models.PositiveIntegerField('Postal code', blank=True, null=True)
    city = models.CharField('City', max_length=40, blank=True, null=True)
    state = models.CharField('State', max_length=40, blank=True, null=True)
    country = models.CharField('Country', max_length=40, blank=True, null=True)
    tax_payer_id = models.CharField('Tax payer id', max_length=40, blank=True, null=True)


class Invoice(models.Model):
    invoice_number = models.CharField('Invoice', max_length=25, editable=False, null=False)
    place = models.CharField('Place', max_length=100)
    issued = models.DateField('Issued')
    due_date = models.DateField('Due date', null=True, editable=False)
    service_date = models.DateTimeField('Service date')
    reference = models.CharField('Reference', max_length=100)
    services = JSONField('Services', default=[])
    total_no_vat = models.DecimalField('Znesek brez DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    total_with_vat = models.DecimalField('Znesek z DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    customer = JSONField('Customer', default=None)
    payed = models.BooleanField('Plačano', default=False)

    def generate_object_number(self, date, last_object):

        if not last_object:
            yr = str(date.year)
            generated_number = '0001-' + yr

        else:
            generated_number = str(int(last_object.invoice_number[:4]) + 1) + last_object.invoice_number[4:]

        return generated_number


    def generate_pdf(self):

        html_context = {
            'services': self.services,
            'invoice_number': self.invoice_number,
            'place': self.place,
            'reference': self.reference,
            'issued': self.issued,
            'due_date': self.due_date,
            'service_date': self.service_date,
            'total_with_vat': self.total_with_vat,
            'total_no_vat': self.total_no_vat,
        }

        pdf_path = create_pdf('invoice.html', html_context, 'invoices', str(self.invoice_number) + '.pdf')

        return pdf_path

    def calculate_total(self):

        total_with_vat = Decimal(str('0.00'))
        total_no_vat = Decimal(str('0.00'))

        for service in self.services:
            service_no_vat = service["price_no_vat"]
            vat = service["vat"]['value']
            total_with_vat = total_with_vat + Decimal(str(service_no_vat)) * (Decimal(str(vat)) + Decimal('1.00'))
            total_no_vat = total_no_vat + Decimal(str(service_no_vat))


        self.total_with_vat = total_with_vat
        self.total_no_vat = total_no_vat


    def save(self, *args, **kwargs):
        if self.invoice_number is None or self.invoice_number == "":
            last_object = Invoice.objects.all().order_by('issued').last()
            self.invoice_number = self.generate_object_number(self.issued, last_object)

        pay_in = timedelta(days=settings.PAYING_PERIOD)
        due_date = self.issued + pay_in
        self.due_date = due_date
        self.calculate_total()

        super(Invoice, self).save(*args, **kwargs)


# class ServicesQuantity(models.Model):
#     invoice = models.ForeignKey(Invoice, blank=False, null=False)
#     service = models.ForeignKey(Service, blank=False, null=False)
#     quantity = models.PositiveIntegerField(default=0)


