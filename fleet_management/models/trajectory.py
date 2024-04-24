from django.db import models
from .taxi import Taxi

class Trajectory(models.Model):
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    date = models.DateTimeField()  # Alterado para DateTimeField
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Trajectory of Taxi {self.taxi_id} at {self.date}"
