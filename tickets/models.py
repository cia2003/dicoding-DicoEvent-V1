from django.db import models

# Create your models here.
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.UUIDField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_start = models.DateTimeField()
    sales_end = models.DateTimeField()
    quota = models.IntegerField()

    def __str__(self):
        return f'Ticket {self.id} for Event {self.event_id}'
    
    class Meta:
        db_table = 'tickets'