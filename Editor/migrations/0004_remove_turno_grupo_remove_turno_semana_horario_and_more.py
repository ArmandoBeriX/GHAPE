# Generated by Django 4.2.16 on 2024-11-28 02:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Recursos', '0005_remove_asignatura_tipo'),
        ('Editor', '0003_remove_turno_horario_turno_grupo_turno_semana_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='semana',
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana', models.PositiveSmallIntegerField()),
                ('balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recursos.balance')),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recursos.grupo')),
            ],
            options={
                'unique_together': {('grupo', 'semana')},
            },
        ),
        migrations.AddField(
            model_name='turno',
            name='horario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='turnos', to='Editor.horario'),
            preserve_default=False,
        ),
    ]
