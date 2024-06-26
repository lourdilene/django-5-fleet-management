import json
from datetime import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import Trajectory
from ..api.taxi_locations import taxi_locations
from django.utils import timezone

class TestTaxiLocationsEndpoint(APITestCase):
    def setUp(self):
        date_with_timezone = timezone.make_aware(datetime(2024, 1, 1))
        self.trajectory1 = Trajectory.objects.create(taxi_id=1, date=date_with_timezone, latitude=10.0, longitude=20.0)
        self.trajectory2 = Trajectory.objects.create(taxi_id=1, date=date_with_timezone, latitude=15.0, longitude=25.0)
        self.trajectory3 = Trajectory.objects.create(taxi_id=1, date=date_with_timezone, latitude=20.0, longitude=30.0)

    def test_taxi_locations_endpoint(self):

        def mock_reverse(viewname, *args, **kwargs):
            kwargs['ordering'] = 'id'
            return f"/api/taxi_locations?{'&'.join([f'{key}={value}' for key, value in kwargs.items()])}"

        taxi_locations.reverse = mock_reverse

        expected_data = [
            {
                'id': self.trajectory1.id,
                'taxi_id': self.trajectory1.taxi_id,
                'date': str(self.trajectory1.date.replace(tzinfo=None)).replace(' ', 'T'),
                'latitude': self.trajectory1.latitude,
                'longitude': self.trajectory1.longitude
            },
            {
                'id': self.trajectory2.id,
                'taxi_id': self.trajectory2.taxi_id,
                'date': str(self.trajectory2.date.replace(tzinfo=None)).replace(' ', 'T'),
                'latitude': self.trajectory2.latitude,
                'longitude': self.trajectory2.longitude
            },
            {
                'id': self.trajectory3.id,
                'taxi_id': self.trajectory3.taxi_id,
                'date': str(self.trajectory3.date.replace(tzinfo=None)).replace(' ', 'T'),
                'latitude': self.trajectory3.latitude,
                'longitude': self.trajectory3.longitude
            }
        ]

        query_params = {'taxi_id': 1, 'date': '2024-01-01'}

        url = reverse('taxi_locations')
        response = self.client.get(url, query_params)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['count'], 3)
        self.assertEqual(response_data['next'], None)
        self.assertEqual(response_data['previous'], None)
        self.assertEqual(response_data['results'], expected_data)
