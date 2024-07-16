from django.db import models
from django.contrib.auth import get_user_model
from activities.models import Activity
from reservations.models import Request

class HistoricalPricingData(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    participants = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity.activity_name} - {self.participants} participants - ${self.price}"
