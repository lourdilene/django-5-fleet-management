from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.urls import reverse
import logging
from ..models.taxi import Taxi

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response(
        'List of taxis',
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
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

    sort_by = request.GET.get('sort_by', 'id')
    ascending = request.GET.get('ascending', 'true').lower() == 'true'

    taxis = taxis.order_by(sort_by) if ascending else taxis.order_by(f'-{sort_by}')

    paginator = Paginator(taxis, CustomPagination().page_size)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    data = [{"id": taxi.id, "plate": taxi.plate} for taxi in page_obj]

    logger = logging.getLogger(__name__)
    logger.debug(f"data: {data}")

    next_page_url = None
    if page_obj.has_next():
        next_page_number = page_obj.next_page_number()
        next_page_url = reverse('get_taxis') + f'?page={next_page_number}&sort_by={sort_by}&ascending={str(ascending).lower()}'

    previous_page_url = None
    if page_obj.has_previous():
        previous_page_number = page_obj.previous_page_number()
        previous_page_url = reverse('get_taxis') + f'?page={previous_page_number}&sort_by={sort_by}&ascending={str(ascending).lower()}'

    return JsonResponse({
        'count': paginator.count,
        'next': next_page_url,
        'previous': previous_page_url,
        'results': data
    }, safe=False)