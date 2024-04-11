from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework.decorators import api_view
from ..models import Trajectory
from ..serializers import TrajectorySerializer

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('taxi_id', openapi.IN_PATH, description='Taxi ID', type=openapi.TYPE_INTEGER),
    ],
    responses={200: openapi.Response(
        'Last taxi location',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'taxi_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'date': openapi.Schema(type=openapi.TYPE_STRING),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE),
            }
        )
    )},
    operation_summary="Get Last Taxi Location",
    operation_description="Get the last location of a taxi."
)
@api_view(['GET'])
def last_taxi_location(request, taxi_id):
    """
    Get the last location of a taxi.
    """
    try:
        last_trajectory = Trajectory.objects.filter(taxi_id=taxi_id).latest('date')
    except Trajectory.DoesNotExist:
        return JsonResponse({'error': 'Taxi not found'}, status=404)

    data = TrajectorySerializer(last_trajectory).data

    return JsonResponse(data)
