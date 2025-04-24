from django.db import models


class MeterReading(models.Model):
    reading_no = models.CharField(max_length=50, db_column='Reading No_',primary_key=True)
    store_no = models.CharField(max_length=50, db_column='Store No_')   
   
    status = models.IntegerField(db_column='Status')  # adjust length
    
    posted_datetime = models.DateTimeField(db_column='Posted DateTime')
    work_date = models.DateField(db_column='Work Date')
    shift_no = models.IntegerField(db_column='Shift No_')  # or IntegerField if it's numeric

    class Meta:
        db_table = '[Emarat Misr$Meter Reading]'
        managed = False  # since it's an external table

    def __str__(self):
        return f"Reading {self.reading_no} - Store {self.store_no}"

        
class MeterReadingLine(models.Model):
   

    reading_no = models.CharField(max_length=50, db_column='Reading No_')
    store_no = models.CharField(max_length=50, db_column='Store No_')
    fuel_item_type = models.CharField(max_length=255)  # assuming it's a string
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    calibration_qty = models.DecimalField(max_digits=10, decimal_places=2)
    customer_sales = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = '[Emarat Misr$Meter Reading Lines]'
        managed = False  # because this is a view or external table

    def __str__(self):
        return f"{self.fuel_item_type} - Qty: {self.qty}"


