# from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404

from core.permissions import IsAdminOrSuperUser
from events.serializers import EventSerializer
from .models import Payment
from .serializers import PaymentSerializer
from django.core.cache import cache

# Create your views here.
CACHE_KEY_LIST = 'payment_list'
CACHE_KEY_DETAIL = 'payment_detail_{}'

class PaymentListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        payments = cache.get(CACHE_KEY_LIST)

        if not payments:
            print("Data diambil dari database")
            data = Payment.objects.all().order_by('id')[:10]
            cache.get(CACHE_KEY_LIST)
            serializer = PaymentSerializer(data, many=True)

            payments_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_LIST, payments_data, timeout=60*60)  # Cache for 1 hour

            payments = payments_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response({'payments':json.loads(payments)})
        response['X-Data-Source'] = data_source
        return response

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_LIST)  # Invalidate cache
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method != 'GET':
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
        payment = cache.get(CACHE_KEY_DETAIL.format(id))

        if not payment:
            print("Data diambil dari database")
            data = self.get_object(id)
            cache.get(CACHE_KEY_DETAIL.format(id))
            serializer = PaymentSerializer(data)

            payment_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_DETAIL.format(id), payment_data, timeout=60*60)  # Cache for 1 hour
            payment = payment_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response(json.loads(payment))
        response['X-Data-Source'] = data_source
        return response

    def put(self, request, id):
        Payment = self.get_object(id)
        serializer = PaymentSerializer(Payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_DETAIL.format(id))
            cache.delete(CACHE_KEY_LIST)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ticket = self.get_object(id)
        ticket.delete()
        cache.delete(CACHE_KEY_DETAIL.format(id))
        cache.delete(CACHE_KEY_LIST)
        return Response(status=status.HTTP_204_NO_CONTENT)