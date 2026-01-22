# from django.shortcuts import render
import datetime
from django.core.cache import cache
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404

from core.permissions import IsAdminOrSuperUser
from events.views import CACHE_KEY_LIST
from .models import Registration
from .serializers import RegistrationSerializer

from .tasks import send_registration_confirmation_email

# Create your views here.
CACHE_KEY_LIST = 'registration_list'
CACHE_KEY_DETAIL = 'registration_detail_{}'

class RegistrationListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        registrations = cache.get(CACHE_KEY_LIST)

        if not registrations:
            print("Data diambil dari database")
            data = Registration.objects.all().order_by('id')
            cache.get(CACHE_KEY_LIST)
            serializer = RegistrationSerializer(data, many=True)
            registrations_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_LIST, registrations_data, timeout=60*60)  # Cache for 1 hour

            registrations = registrations_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response({'registrations':json.loads(registrations)})
        response['X-Data-Source'] = data_source
        return response

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            registration = serializer.save()
            order_datetime = registration.ticket.event.start_time
            order_time = order_datetime.hour

            now_datetime = datetime.now()
            now_time = now_datetime.hour

            time_difference = order_time - now_time

            if time_difference == 2:
                send_registration_confirmation_email.delay(
                    user_email=registration.user.email,
                    username=registration.user.username,
                    registration_id=registration.id, 
                    time=time_difference
                )
            else:
                send_registration_confirmation_email.delay(
                    user_email=registration.user.email,
                    username=registration.user.username,
                    registration_id=registration.id, 
                )
            cache.delete(CACHE_KEY_LIST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method != 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get_object(self, id):
        try:
            event = Registration.objects.get(id=id)
            self.check_object_permissions(self.request, event)
            return event
        except Registration.DoesNotExist:
            raise Http404

    def get(self, request, id):
        registration = cache.get(CACHE_KEY_DETAIL.format(id))

        if not registration:
            print("Data diambil dari database")
            data = self.get_object(id)
            cache.get(CACHE_KEY_DETAIL.format(id))
            serializer = RegistrationSerializer(data)
            registration_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_DETAIL.format(id), registration_data, timeout=60*60)  # Cache for 1 hour
            registration = registration_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response(json.loads(registration))
        response['X-Data-Source'] = data_source
        return response

    def put(self, request, id):
        registration = self.get_object(id)
        serializer = RegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_DETAIL.format(id))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ticket = self.get_object(id)
        ticket.delete()
        cache.delete(CACHE_KEY_DETAIL.format(id))
        return Response(status=status.HTTP_204_NO_CONTENT)