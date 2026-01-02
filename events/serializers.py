from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'location', 'start_time', 'end_time',
            'status', 'quota', 'category', 'organizer_id', 'url'
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