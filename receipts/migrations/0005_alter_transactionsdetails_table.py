# Generated by Django 5.0.14 on 2025-04-24 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0004_historicaldata_transactionsdetails'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='transactionsdetails',
            table='receipts_TransactionsDetails',
        ),
    ]
