import django
import pytest
from django.test import RequestFactory
import os
from django.conf import settings

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleet_management.settings')

    django.setup()

@pytest.fixture
def api_rf():
    return RequestFactory()
