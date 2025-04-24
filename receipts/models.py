from django.db import models

# Create your models here.

class Receipt(models.Model):
    """
    Model to represent a receipt.
    """
    receipt_number = models.CharField(max_length=20, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    branch = models.CharField(max_length=100)

    def __str__(self):
        return f"Receipt {self.receipt_number} - {self.branch}"
    
    class Store(models.Model):
        """
        Model to represent a store.
        """
        store_id = models.CharField(max_length=20, unique=True)
        store_name = models.CharField(max_length=100)
        historical_storecode=models.CharField(max_length=20, blank=True, null=True)
            
        def __str__(self):
                return self.store_name
            
    class GasolineProducts(models.Model):
        """
        Model to represent a store.
        """
        product_code = models.CharField(max_length=20, unique=True)
        product_name = models.CharField(max_length=100)
        historical_productcode=models.CharField(max_length=20, blank=True, null=True)
            
        def __str__(self):
                return self.product_code

  

class HistoricalData(models.Model):
    id = models.AutoField(primary_key=True)
    station_code = models.CharField(max_length=50, db_column='StationCode')
    station_name = models.CharField(max_length=100, db_column='StationName')
    start_date = models.DateTimeField(db_column='StartDate')
    end_date = models.DateTimeField(db_column='EndDate')
    date = models.DateField(db_column='Date')
    hour = models.IntegerField(db_column='Hour')
    pump_id = models.IntegerField(db_column='PumpId')
    hose_id = models.IntegerField(db_column='HoseId')
    volume = models.DecimalField(max_digits=10, decimal_places=2, db_column='Volume')
    ppu = models.DecimalField(max_digits=10, decimal_places=3, db_column='Ppu')
    money = models.DecimalField(max_digits=12, decimal_places=2, db_column='Money')
    grade_id = models.IntegerField(db_column='GradeId')
    product = models.CharField(max_length=50, db_column='Product')

    class Meta:
        db_table = 'HistoricalData'
        managed = False  # if table already exists in the database

    def __str__(self):
        return f"{self.station_name} - {self.station_code} {self.date}"

class TransactionsDetails(models.Model):
    id = models.AutoField(primary_key=True)  # Assuming it's the table's primary key
    station_code = models.CharField(max_length=50)
    station_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    date = models.DateField()
    hour = models.IntegerField()
    pump_id = models.IntegerField()
    hose_id = models.IntegerField()
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    ppu = models.DecimalField(max_digits=10, decimal_places=3)  # Price per unit
    money = models.DecimalField(max_digits=12, decimal_places=2)
    grade_id = models.IntegerField()
    product = models.CharField(max_length=50)
    transBatchID = models.CharField(max_length=50,default='01-2009-2022-09-02')
    shift = models.IntegerField(default=1)

    class Meta:
        db_table = 'receipts_TransactionsDetails'
        managed = True  # if table already exists in the database

    def __str__(self):
        return f"{self.station_name} - {self.station_code} {self.date}"
    
    
class TransactionLog(models.Model):
        """
        Model to represent a store.
        """
        autoID=models.AutoField(primary_key=True)
        store_name = models.CharField(max_length=100)
        store_id = models.CharField(max_length=20)
        meterReadingNo = models.CharField(max_length=100)
        shiftNo=models.CharField(max_length=20, blank=True, null=True)
        productCode=models.CharField(max_length=20, blank=True, null=True)
        totalVolume=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
        calcVolume=models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
        numberOfRecords=models.IntegerField(blank=True, null=True)
        dateTimeRunOn = models.DateTimeField(auto_now_add=True)   
        def __str__(self):
                return self.store_name
       
