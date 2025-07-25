# Generated by Django 5.0.14 on 2025-05-04 06:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0010_rename_shiftnumb_store_shiftcount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='first_shift_end',
        ),
        migrations.RemoveField(
            model_name='store',
            name='first_shift_start',
        ),
        migrations.RemoveField(
            model_name='store',
            name='g80',
        ),
        migrations.RemoveField(
            model_name='store',
            name='g92',
        ),
        migrations.RemoveField(
            model_name='store',
            name='g95',
        ),
        migrations.RemoveField(
            model_name='store',
            name='go',
        ),
        migrations.RemoveField(
            model_name='store',
            name='second_shift_end',
        ),
        migrations.RemoveField(
            model_name='store',
            name='second_shift_start',
        ),
        migrations.RemoveField(
            model_name='store',
            name='third_shift_end',
        ),
        migrations.RemoveField(
            model_name='store',
            name='third_shift_start',
        ),
        migrations.AddField(
            model_name='store',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='store',
            name='rin',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='store_address',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
    ]
