"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GHAPE.settings')

application = get_wsgi_application()
"""



import os
import sys

path = '/home/ArmandoBeriX/GHAPE'  # Ruta de tu proyecto
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'GHAPE.settings'  # Cambia 'tu_proyecto' al nombre de tu proyecto Django

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()