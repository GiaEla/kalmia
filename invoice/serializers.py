from rest_framework import serializers

from invoice.models import Invoice, Service, UserProfile, ServicesQuantity


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 2


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class ServicesQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesQuantity
        fields = '__all__'
        depth = 1
