import json
from django.urls import reverse
from ..api.taxi import get_taxis

# @pytest.mark.django_db
def test_get_taxis(api_rf):

    request = api_rf.get(reverse('get_taxis'))
    response = get_taxis(request)

    assert response.status_code == 200

    data = response.content.decode('utf-8')  
    data_dict = json.loads(data)

    assert 'count' in data_dict
    assert 'next' in data_dict
    assert 'previous' in data_dict
    assert 'results' in data_dict

    assert len(data_dict['results']) == 10  
    assert data_dict['count'] == 10320  

    next_page_url = data_dict['next']
    request = api_rf.get(next_page_url)
    next_page_response = get_taxis(request)

    assert next_page_response.status_code == 200

    next_page_data = json.loads(next_page_response.content.decode('utf-8'))

    assert 'count' in next_page_data
    assert 'next' in next_page_data
    assert 'previous' in next_page_data
    assert 'results' in next_page_data

    assert len(next_page_data['results']) == 10
