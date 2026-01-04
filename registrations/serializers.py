from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import User
from tickets.models import Ticket
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    ticket = serializers.CharField(source='ticket.id', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        write_only=True,
        source='ticket'
    )

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),    
        write_only=True,
        source='user'
    )

    class Meta:
        model = Registration
        fields = [
            'id', 'ticket', 'ticket_id', 'user', 'user_id', 'url'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return [
            {
                "rel": "self",
                "href": reverse('event-list', request=request), 
                "action": "POST", 
                "types": ["application/json"]
            }, 
            {
                "rel": "self",
                "href": reverse('event-detail', kwargs={'id': obj.id}, request=request), 
                "action": "GET", 
                "types": ["application/json"]
            }, 
            {
                "rel": "self",
                "href": reverse('event-detail', kwargs={'id': obj.id}, request=request), 
                "action": "PUT", 
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('event-detail', kwargs={'id': obj.id}, request=request), 
                "action": "DELETE", 
                "types": ["application/json"]
            }
        ]