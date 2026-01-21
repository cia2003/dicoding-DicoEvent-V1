import json
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import Group
from .models import User
from .serializers import UserSerializer
from .serializers import GroupSerializer
from .permissions import IsAdminOrSuperUser, IsOwnerOrAdminOrSuperUser, IsSuperUser
 

CACHE_KEY_LIST = 'user_list'
CACHE_KEY_DETAIL = 'user_detail_{}'

class UserListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return []
    
    def get(self, request):
        users = cache.get(CACHE_KEY_LIST)

        if not users:
            print("Data diambil dari database")
            data = User.objects.all().order_by('username')[:10]
            cache.get(CACHE_KEY_LIST)
            serializer = UserSerializer(data, many=True)
            users_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_LIST, users_data, timeout=60*60)  # Cache for 1 hour
            users = users_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response({'users':json.loads(users)})
        response['X-Data-Source'] = data_source
        return response
 
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_LIST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated(), IsOwnerOrAdminOrSuperUser()]
        
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404
 
    def get(self, request, pk):
        user = cache.get(CACHE_KEY_DETAIL.format(pk))

        if not user:
            print("Data diambil dari database")
            data = self.get_object(pk)
            cache.get(CACHE_KEY_DETAIL.format(pk))
            serializer = UserSerializer(data)
            user_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_DETAIL.format(pk), user_data, timeout=60*60)  # Cache for 1 hour
            user = user_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response(json.loads(user))
        response['X-Data-Source'] = data_source
        return response
 
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_DETAIL.format(pk))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        cache.delete(CACHE_KEY_DETAIL.format(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GroupListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        return [IsAuthenticated(), IsSuperUser()]

    def get(self, request):
        groups = cache.get(CACHE_KEY_LIST)

        if not groups:
            print("Data diambil dari database")
            data = Group.objects.all().order_by('name')[:10]
            cache.get(CACHE_KEY_LIST)
            serializer = GroupSerializer(data, many=True)
            groups_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_LIST, groups_data, timeout=60*60)  # Cache for 1 hour
            groups = groups_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response({'groups':json.loads(groups)})
        response['X-Data-Source'] = data_source
        return response
 
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_LIST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class GroupDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        return [IsAuthenticated(), IsSuperUser()]
    
    def get_object(self, pk):
        try:
            group = Group.objects.get(pk=pk)
            self.check_object_permissions(self.request, group)
            return group
        except Group.DoesNotExist:
            raise Http404
 
    def get(self, request, pk):
        group = cache.get(CACHE_KEY_LIST)

        if not group:
            print("Data diambil dari database")
            data = self.get_object(pk)
            cache.get(CACHE_KEY_DETAIL.format(pk))
            serializer = GroupSerializer(data)
            group_data = json.dumps(serializer.data, default=str)
            cache.set(CACHE_KEY_DETAIL.format(pk), group_data, timeout=60*60)  # Cache for 1 hour
            group = group_data
            data_source = "database"
        else:
            print("Data diambil dari cache")
            data_source = "cache"

        response = Response(json.loads(group))
        response['X-Data-Source'] = data_source
        return response
 
    def put(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_DETAIL.format(pk))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        group = self.get_object(pk)
        group.delete()
        cache.delete(CACHE_KEY_DETAIL.format(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignRoleView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        return [IsAuthenticated(), IsSuperUser()]
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.data['user_id'])
        group = get_object_or_404(Group, pk=request.data['group_id'])
        user.groups.add(group)
        return Response(
            {
                "message": "Role assigned successfully",
                "user_id": str(user.id),
                "group": group.name
            },
            status=status.HTTP_201_CREATED
        )