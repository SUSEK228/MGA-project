# Generated by Django 5.2.1 on 2025-05-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0005_task_created_by_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Nowy', 'Nowy'), ('W toku', 'W toku'), ('Rozwiązany', 'Rozwiązany')], default='Nowy', max_length=50),
        ),
    ]
