from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.urls import reverse
from ..models import Trajectory
import logging
from ..serializers import TrajectorySerializer
from datetime import datetime

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('taxi_id', openapi.IN_QUERY, description='Taxi ID', type=openapi.TYPE_INTEGER),
        openapi.Parameter('date', openapi.IN_QUERY, description='Date in YYYY-MM-DD format', type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
        openapi.Parameter('ordering', openapi.IN_QUERY, description='Field to order by', type=openapi.TYPE_STRING),
    ],
    responses={200: openapi.Response(
        'List of trajectories',
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'taxi_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'date': openapi.Schema(type=openapi.TYPE_STRING),
                    'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE),
                    'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE),
                }
            )
        )
    )},
    operation_summary="Get Taxi Locations",
    operation_description="Get a list of all taxi locations for a given taxi ID and date."
)
@api_view(['GET'])
def taxi_locations(request):
    """
    Get a list of all taxi locations for a given taxi ID and date.
    """
    query_params = request.query_params
    taxi_id = query_params.get('taxi_id')
    date_str = query_params.get('date')

    #date_str = '2008-02-08'

    # Converter a string 'date' em um objeto datetime
    date = datetime.strptime(date_str, '%Y-%m-%d')

    if taxi_id is None or date is None:
        return JsonResponse({'error': 'taxi_id and date are required'}, status=400)

    ordering = query_params.get('ordering', None)

    trajectories = Trajectory.objects.filter(taxi_id=taxi_id, date__date=date.date()).order_by('id')
    if ordering:
        trajectories = trajectories.order_by(ordering)

    paginator = Paginator(trajectories, CustomPagination().page_size)
    page_number = query_params.get('page')
    page_obj = paginator.get_page(page_number)

    logger = logging.getLogger(__name__)
    logger.debug(f"page_obj: {TrajectorySerializer(page_obj, many=True).data}")

    data = TrajectorySerializer(page_obj, many=True).data

    next_page_url = None
    if page_obj.has_next():
        next_page_number = page_obj.next_page_number()
        next_page_url = reverse('taxi_locations') + f'?page={next_page_number}&taxi_id={taxi_id}&date={date}'

    previous_page_url = None
    if page_obj.has_previous():
        previous_page_number = page_obj.previous_page_number()
        previous_page_url = reverse('taxi_locations') + f'?page={previous_page_number}&taxi_id={taxi_id}&date={date}'

    return JsonResponse({
        'count': paginator.count,
        'next': next_page_url,
        'previous': previous_page_url,
        'results': data
    }, safe=False)
