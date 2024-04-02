from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework.decorators import api_view
from ..models.taxi import Taxi

@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response
               ('List of taxis', schema=openapi.Schema
                    (type=openapi.TYPE_ARRAY, items=openapi.Schema
                        (type=openapi.TYPE_OBJECT, properties=
                            {
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'plate': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    )
                )},
    operation_summary="Get Taxis",
    operation_description="Get a list of all taxis."
)
@api_view(['GET'])
def get_taxis(request):
    """
    Get a list of all taxis.
    """
    taxis = Taxi.objects.all()
    data = [{"id": taxi.id, "plate": taxi.plate} for taxi in taxis]
    return JsonResponse(data, safe=False)
