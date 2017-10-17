# Create your views here.
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from invoice.models import Invoice
from invoice.serializers import InvoiceSerializer


class InvoiceApi(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, invoice_id, format=None):
        invoice = Invoice.objects.get(id=invoice_id)
        invoice_serializer = InvoiceSerializer(invoice)

        return Response(invoice_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = InvoiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, invoice_id, format=None):

        invoice = Invoice.objects.get(id=invoice_id)

        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceListApi(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        invoice_list = Invoice.objects.all()
        invoice_list_serializer = InvoiceSerializer(invoice_list, many=True)

        return Response(invoice_list_serializer.data, status=status.HTTP_200_OK)