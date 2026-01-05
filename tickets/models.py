import uuid
from django.db import models
from events.models import Event

# Create your models here.
class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    sales_start = models.DateTimeField()
    sales_end = models.DateTimeField()
    quota = models.IntegerField()

    def __str__(self):
        return f'Ticket {self.id} for Event {self.event_id}'
    
    class Meta:
        db_table = 'tickets'