from django.db import models
import uuid

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=300)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    quota = models.IntegerField()
    category = models.CharField(max_length=100)
    organizer_id = models.UUIDField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'events'