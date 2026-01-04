from rest_framework import serializers
from rest_framework.reverse import reverse

from events.models import Event
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        write_only=True,
        source='event'
    )

    event = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = [
            'id', 'event', 'event_id', 'name', 'price', 'sales_start', 'sales_end', 'quota', 'url'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return [
            {
                "rel": "self",
                "href": reverse('ticket-list', request=request), 
                "action": "POST", 
                "types": ["application/json"]
            }, 
            {
                "rel": "self",
                "href": reverse('ticket-detail', kwargs={'id': obj.id}, request=request), 
                "action": "GET", 
                "types": ["application/json"]
            }, 
            {
                "rel": "self",
                "href": reverse('ticket-detail', kwargs={'id': obj.id}, request=request), 
                "action": "PUT", 
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('ticket-detail', kwargs={'id': obj.id}, request=request), 
                "action": "DELETE", 
                "types": ["application/json"]
            }
        ]