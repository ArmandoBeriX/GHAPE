from django.apps import AppConfig


class EditorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Editor'
    

class RecursosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Recursos'
    verbose_name='Recursos Disponibles'

class CuentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cuentas'
    verbose_name='cuentas'

def ready(self):
    import Editor.signals