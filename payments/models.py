import uuid
from django.db import models

from registrations.models import Registration

# Create your models here.
class Payment(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    amount_paid = models.IntegerField()

    def __str__(self):
        return f"{self.amount_paid} - {self.payment_status}"
    
    class Meta:
        db_table = 'payments'