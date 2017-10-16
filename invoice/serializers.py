from rest_framework import serializers

from invoice.models import Invoice, Service, ServicesQuantity, Vat, Customer


class VatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vat
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 2


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        depth = 1


class CostumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ServicesQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesQuantity
        fields = '__all__'
        depth = 3
