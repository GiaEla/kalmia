from django.contrib import admin

from invoice.models import Invoice, ServicesQuantity, Customer, Service, Vat


class ServiceQuantityInline(admin.StackedInline):
    model = ServicesQuantity
    extra = 0


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ServiceQuantityInline]

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Vat)
