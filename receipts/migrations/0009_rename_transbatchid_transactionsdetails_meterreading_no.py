# Generated by Django 5.0.14 on 2025-04-26 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0008_remove_store_historical_storecode_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionsdetails',
            old_name='transBatchID',
            new_name='meterreading_no',
        ),
    ]
