# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404

from core.permissions import IsAdminOrSuperUser, IsOrganizerOrAdmin, IsOrganizerOrAdminOrSuperUser
from .models import Ticket
from .serializers import TicketSerializer

# Create your views here.
class TicketListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsOrganizerOrAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        tickets = Ticket.objects.all().order_by('sales_start')[:10]
        serializer = TicketSerializer(tickets, many=True)
        return Response({'tickets': serializer.data})

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        admin_superuser_access = ['PUT', 'DELETE']

        if self.request.method in admin_superuser_access:
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get_object(self, id):
        try:
            event = Ticket.objects.get(id=id)
            self.check_object_permissions(self.request, event)
            return event
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, id):
        ticket = self.get_object(id)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, id):
        ticket = self.get_object(id)
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ticket = self.get_object(id)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)