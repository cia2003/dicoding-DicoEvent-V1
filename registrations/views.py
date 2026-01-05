# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404

from core.permissions import IsAdminOrSuperUser
from .models import Registration
from .serializers import RegistrationSerializer

# Create your views here.
class RegistrationListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        registrations = Registration.objects.all().order_by('id')
        serializer = RegistrationSerializer(registrations, many=True)
        return Response({'registrations': serializer.data})

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        registration = self.get_object(id)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)

    def put(self, request, id):
        registration = self.get_object(id)
        serializer = RegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ticket = self.get_object(id)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)