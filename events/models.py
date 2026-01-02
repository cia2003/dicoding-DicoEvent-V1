from django.db import models
import uuid

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'events'