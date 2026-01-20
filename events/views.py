# from django.shortcuts import render
import os
import tempfile
from django.shortcuts import get_object_or_404
from minio import Minio
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404

from core.permissions import IsOrganizerOrAdminOrSuperUser, IsOrganizerOwnerOrAdminOrSuperUser
from .models import Event
from .serializers import EventPosterSerializer, EventSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
def get_minio_client():
    return Minio(
        endpoint=os.getenv('MINIO_ENDPOINT_URL'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False
    )

bucket_name = os.getenv('MINIO_BUCKET_NAME')

class EventListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsOrganizerOrAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        events = Event.objects.all().order_by('start_time')[:10]
        serializer = EventSerializer(events, many=True)
        return Response({'events': serializer.data})

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method != 'GET':
            return [IsAuthenticated(), IsOrganizerOwnerOrAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get_object(self, id):
        try:
            event = Event.objects.get(id=id)
            self.check_object_permissions(self.request, event)
            return event
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, id):
        event = self.get_object(id)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, id):
        event = self.get_object(id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        event = self.get_object(id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventPosterView(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        return [isAuthenticated(), IsOrganizerOwnerOrAdminOrSuperUser()]
    
    def post(self, request):
        serializer = EventPosterSerializer(data=request.data)
        file = request.data.get('image')

        if serializer.is_valid():
            serializer.save()

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            try:
                object_name = f"{serializer.instance.image.name}"
                client = get_minio_client()
                client.fput_object(bucket_name, object_name, temp_file_path, content_type=file.content_type)
            except Exception as e:
                return Response(
                    {"error": f"Upload to Minio failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                os.remove(temp_file_path)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

class EventPosterDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        images = event.eventimage_set.all()

        serialized_images = []
        for image in images:
            client = get_minio_client()
            presigned_url = client.presigned_get_object(
                bucket_name,
                image.image_name,
                response_headers={"response-content-type": "image/jpeg"}
            )
            serialized_images.append({
                'id': image.id,
                'url': presigned_url
            })

        return Response(serialized_images)