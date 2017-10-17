from django.contrib import admin

from invoice.models import Invoice, Customer, Service, Vat

admin.site.register(Invoice)
admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Vat)
