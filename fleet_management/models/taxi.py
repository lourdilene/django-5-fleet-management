# models.py

from django.db import models

class Taxi(models.Model):
    id = models.AutoField(primary_key=True)
    plate = models.CharField(max_length=20)

    def __str__(self):
        return f"Taxi {self.id}: {self.plate}"
