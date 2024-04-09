from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Trajectory
import json

class TestLastTaxiLocation(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.taxi_id = 1
        self.trajectory = Trajectory.objects.create(taxi_id=self.taxi_id, date='2024-01-01', latitude=10.0, longitude=20.0)

    def test_get_last_taxi_location(self):
        url = reverse('last_taxi_location', kwargs={'taxi_id': self.taxi_id})
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.trajectory.id)
        self.assertEqual(response_data['taxi_id'], self.trajectory.taxi_id)
        self.assertEqual(response_data['date'], '2024-01-01')
        self.assertEqual(response_data['latitude'], 10.0)
        self.assertEqual(response_data['longitude'], 20.0)

    def test_get_last_taxi_location_not_found(self):
        non_existing_taxi_id = 999
        url = reverse('last_taxi_location', kwargs={'taxi_id': non_existing_taxi_id})
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Taxi not found')
