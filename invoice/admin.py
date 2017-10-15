from django.contrib import admin

from invoice.models import Invoice, ServicesQuantity


class ServiceQuantityInline(admin.StackedInline):
    model = ServicesQuantity
    extra = 0


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ServiceQuantityInline]

admin.site.register(Invoice, InvoiceAdmin)
