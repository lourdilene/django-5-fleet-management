from rest_framework import serializers
from .models import Trajectory
from datetime import datetime

class DateField(serializers.Field):
    """
    Serializer field for handling datetime fields as dates.
    """
    def to_representation(self, value):
        # Convertendo o objeto datetime em uma string no formato ISO 8601
        return value.timestamp() if value else None

class TrajectorySerializer(serializers.ModelSerializer):
    date = DateField()

    class Meta:
        model = Trajectory
        fields = ['id', 'taxi_id', 'date', 'latitude', 'longitude']

    def to_representation(self, instance):
        # Sobrescrevendo o método para garantir que todos os campos são serializados corretamente
        ret = super().to_representation(instance)
        ret['date'] = DateField().to_representation(instance.date)
        return ret
