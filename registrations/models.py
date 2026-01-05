import uuid
from django.db import models

from core.models import User
from tickets.models import Ticket

# Create your models here.
class Registration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Registration {self.id} for Event {self.ticket}'

    class Meta:
        db_table = 'registrations'