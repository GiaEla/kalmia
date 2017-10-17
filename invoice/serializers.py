from rest_framework import serializers

from invoice.models import Invoice, Service, Vat, Customer


class VatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vat
        fields = '__all__'


class CostumerSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=Customer()._meta.get_field('id'))

    class Meta:
        model = Customer
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):

    id = serializers.ModelField(model_field=Service()._meta.get_field('id'))
    vat = VatSerializer()

    class Meta:
        model = Service
        fields = '__all__'
        depth = 1


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1