# from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404

from core.permissions import IsAdminOrSuperUser, IsOrganizerOrAdmin, IsOrganizerOrAdminOrSuperUser
from .models import Ticket
from .serializers import TicketSerializer
from django.core.cache import cache

# Create your views here.
CACHE_KEY_LIST = 'ticket_list'
CACHE_KEY_DETAIL = 'ticket_detail_{}'
class TicketListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsOrganizerOrAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        tickets = cache.get(CACHE_KEY_LIST)

        if not tickets:
            print("Data diambil dari database")
            data = Ticket.objects.all().order_by('sales_start')[:10]
            cache.get(CACHE_KEY_LIST)
            serializer = TicketSerializer(data, many=True)

            tickets_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_LIST, tickets_data, timeout=60*60)  # Cache for 1 hour

            tickets = tickets_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response({'tickets':json.loads(tickets)})
        response['X-Data-Source'] = data_source
        return response

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_LIST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method != 'GET':
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
        ticket = cache.get(CACHE_KEY_DETAIL.format(id))

        if not ticket:
            print("Data diambil dari database")
            data = self.get_object(id)
            cache.get(CACHE_KEY_DETAIL.format(id))
            serializer = TicketSerializer(data)
            ticket_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_DETAIL.format(id), ticket_data, timeout=60*60)  # Cache for 1 hour
            ticket = ticket_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response(json.loads(ticket))
        response['X-Data-Source'] = data_source
        return response

    def put(self, request, id):
        ticket = self.get_object(id)
        serializer = TicketSerializer(ticket, data=request.data)
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