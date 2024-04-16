from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from ..models import Trajectory
from celery import shared_task
from openpyxl import Workbook
from django.core.files.base import ContentFile
from ..lib import Smtp
import logging
import os
from io import BytesIO

@api_view(['GET'])
def download_excel(request):
    file_identifier = request.query_params.get('file_identifier')
    file_path = f'/home/lour/python-projects/fleet_management/generated_files/{file_identifier}_trajectories.xlsx'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={file_identifier}_trajectories.xlsx'
            return response
    else:
        return JsonResponse({'error': 'File not found.'}, status=404)
