from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *

@receiver(post_save, sender=Cuenta)
def agregar_a_usuarios(sender, instance, created, **kwargs):
    if created:
        try:
            usuarios = Group.objects.get(name='usuario')
        except Group.DoesNotExist:
            usuarios  = Group.objects.create(name='usuario')
        instance.usuario.groups.add(usuarios)