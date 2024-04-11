from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from ..models import Trajectory
from celery import shared_task
from openpyxl import Workbook
from django.core.files.base import ContentFile
import logging
import os
from io import BytesIO

@api_view(['GET'])
def export_to_excel(request):
    query_params = request.query_params
    taxi_id = query_params.get('taxi_id')
    date = query_params.get('date')

    file_identifier = f"{taxi_id}_{date}"

    generate_excel_task.delay(taxi_id, date, file_identifier)

    return JsonResponse({'message': 'Excel generation started.', 'file_identifier': file_identifier})


@shared_task
def generate_excel_task(taxi_id, date, file_identifier):

    # logger = logging.getLogger(__name__)
    # logger.debug(f"file_identifier: {file_identifier}")
    
    trajectories = Trajectory.objects.filter(taxi_id=taxi_id, date=date)

    wb = Workbook()
    ws = wb.active

    ws.append(['Latitude', 'Longitude'])

    for trajectory in trajectories:
        ws.append([trajectory.latitude, trajectory.longitude])

    excel_content = BytesIO()
    wb.save(excel_content)

    excel_content_file = ContentFile(excel_content.getvalue())

    logger = logging.getLogger(__name__)
    logger.debug(f"excel_content: {excel_content}")

    file_path = f'/home/lour/python-projects/fleet_management/generated_files/{file_identifier}_trajectories.xlsx'

    with open(file_path, 'wb') as f:
        f.write(excel_content_file.read())

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
