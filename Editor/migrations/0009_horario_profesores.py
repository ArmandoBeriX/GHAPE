# Generated by Django 5.2 on 2025-05-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Editor', '0008_remove_horario_profesores_ids'),
        ('Recursos', '0011_alter_profesor_options_remove_profesor_grupos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='profesores',
            field=models.ManyToManyField(blank=True, related_name='horarios', to='Recursos.profesor'),
        ),
    ]
