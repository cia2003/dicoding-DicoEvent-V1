# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404

from core.permissions import IsAdminOrSuperUser
from .models import Payment
from .serializers import PaymentSerializer

# Create your views here.
class PaymentListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        Payments = Payment.objects.all().order_by('id')
        serializer = PaymentSerializer(Payments, many=True)
        return Response({'Payments': serializer.data})

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        admin_superuser_access = ['PUT', 'DELETE']
        
        if self.request.method in admin_superuser_access:
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get_object(self, id):
        try:
            event = Payment.objects.get(id=id)
            self.check_object_permissions(self.request, event)
            return event
        except Payment.DoesNotExist:
            raise Http404

    def get(self, request, id):
        Payment = self.get_object(id)
        serializer = PaymentSerializer(Payment)
        return Response(serializer.data)

    def put(self, request, id):
        Payment = self.get_object(id)
        serializer = PaymentSerializer(Payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ticket = self.get_object(id)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)