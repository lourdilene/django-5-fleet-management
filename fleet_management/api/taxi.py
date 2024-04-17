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

def validate_sort_order(sort_by, ascending):
    valid_fields = ['id', 'plate']
    if sort_by not in valid_fields:
        sort_by = 'id'
    if ascending.lower() not in ['true', 'false']:
        ascending = 'true'
    return sort_by, ascending

def get_paginated_taxis(queryset, page_number, sort_by, ascending):
    sort_by, ascending = validate_sort_order(sort_by, ascending)
    taxis = queryset.order_by(sort_by) if ascending == 'true' else queryset.order_by(f'-{sort_by}')
    paginator = Paginator(taxis, CustomPagination().page_size)
    page_obj = paginator.get_page(page_number)
    return page_obj

def prepare_response_data(page_obj):
    data = [{"id": taxi.id, "plate": taxi.plate} for taxi in page_obj]
    return data

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('sort_by', openapi.IN_QUERY, description='Field to sort by (id, plate)', type=openapi.TYPE_STRING),
        openapi.Parameter('ascending', openapi.IN_QUERY, description='Whether to sort ascending or descending (true, false)', type=openapi.TYPE_BOOLEAN),
        openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
    ],
    responses={200: openapi.Response(
        'List of taxis',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                'next': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'previous': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'plate': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                ),
            }
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
    try:
        sort_by = request.GET.get('sort_by', 'id')
        ascending = request.GET.get('ascending', 'true')
        page_number = request.GET.get('page')

        taxis_queryset = Taxi.objects.all()
        page_obj = get_paginated_taxis(taxis_queryset, page_number, sort_by, ascending)

        data = prepare_response_data(page_obj)

        next_page_url = None
        previous_page_url = None
        if page_obj.has_next():
            next_page_url = reverse('get_taxis') + f'?page={page_obj.next_page_number()}&sort_by={sort_by}&ascending={ascending}'
        if page_obj.has_previous():
            previous_page_url = reverse('get_taxis') + f'?page={page_obj.previous_page_number()}&sort_by={sort_by}&ascending={ascending}'

        return JsonResponse({
            'count': page_obj.paginator.count,
            'next': next_page_url,
            'previous': previous_page_url,
            'results': data
        }, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
