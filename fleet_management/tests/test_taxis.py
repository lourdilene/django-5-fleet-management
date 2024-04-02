import json
import django
from django.test import RequestFactory
from ..api.taxi import get_taxis

def test_get_taxis():

    factory = RequestFactory()
    request = factory.get('/get_taxis/')
    response = get_taxis(request)

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    data = json.loads(response.content)

    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)
    assert all('id' in item and 'plate' in item for item in data)
