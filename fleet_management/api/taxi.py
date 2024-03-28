# views.py

from django.http import JsonResponse
from ..models.taxi import Taxi

def get_taxis(request):
    taxis = Taxi.objects.all()
    data = [{"id": taxi.id, "plate": taxi.plate} for taxi in taxis]
    return JsonResponse(data, safe=False)
