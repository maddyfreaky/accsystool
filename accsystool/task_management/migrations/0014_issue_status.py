# Generated by Django 5.1 on 2024-09-13 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0013_remove_todolist_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('todo', 'To Do'), ('progress', 'In Progress'), ('done', 'Done')], default='todo', max_length=10),
        ),
    ]
