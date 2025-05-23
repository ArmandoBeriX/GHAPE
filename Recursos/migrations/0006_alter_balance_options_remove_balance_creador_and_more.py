# Generated by Django 5.1.6 on 2025-04-22 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recursos', '0005_remove_asignatura_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='balance',
            options={'permissions': [('can_manage_balances', 'Puede gestionar semanas académicas')]},
        ),
        migrations.RemoveField(
            model_name='balance',
            name='creador',
        ),
        migrations.AlterField(
            model_name='balance',
            name='dia_fin',
            field=models.DateField(unique=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='dia_inicio',
            field=models.DateField(unique=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='numero_semana',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
