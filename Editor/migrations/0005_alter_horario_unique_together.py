# Generated by Django 4.2.16 on 2024-11-28 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Editor', '0004_remove_turno_grupo_remove_turno_semana_horario_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='horario',
            unique_together=set(),
        ),
    ]
