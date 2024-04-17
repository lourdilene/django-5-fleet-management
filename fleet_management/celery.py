# celery.py
import os
from celery import Celery

# Configurações padrão do Django para uso com Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleet_management.settings')

app = Celery('fleet_management')

# Configuração das opções do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar tarefas de aplicativos Django
app.autodiscover_tasks()
