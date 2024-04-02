import django
import pytest

def pytest_configure():
    django.setup()
