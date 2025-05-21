import datetime
from django.db import models
from django.contrib.auth.models import User
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
    latest_used_Receipt=models.CharField(max_length=100, blank=True, null=True,default='000201-P00000000001')
    shiftcount=models.IntegerField(default=3, blank=True, null=True)
    store_address = models.TextField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    rin = models.CharField(max_length=20, blank=True, null=True)
    
    
        
    def __str__(self):
            return self.store_name
        
class StationDailyClosedPeriods(models.Model):
    """
    Model to represent a store.
    """
    incrID = models.AutoField(primary_key=True)
    store = models.ForeignKey(
    'Store',  # or use the full app label like 'yourapp.Store'
    to_field='store_id',  # assuming store_id is the primary key
    on_delete=models.CASCADE
)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(default=datetime.datetime.now)
    
    def __str__(self):
            return f"{self.store_id} - {self.start_date} to {self.end_date}"
    
        
    
            
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
    receiptNo = models.CharField(max_length=50,default='000201-P00000000001') #template 0000501-P0000553988
    station_code = models.CharField(max_length=50)
    station_name = models.CharField(max_length=100,null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    date = models.DateField()
    hour = models.IntegerField(null=True, blank=True)
    pump_id = models.IntegerField(null=True, blank=True)
    hose_id = models.IntegerField(null=True, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    ppu = models.DecimalField(max_digits=10, decimal_places=3,null=True, blank=True)  # Price per unit
    money = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True)
    grade_id = models.IntegerField(null=True, blank=True)
    product = models.CharField(max_length=50)
    meterreading_no = models.CharField(max_length=50,default='01-2009-2022-09-02')
    shift = models.IntegerField(default=1,null=True, blank=True)
    is_adjustment=models.BooleanField(default=False)  # Assuming this is a boolean field
    created_at = models.DateTimeField(default=datetime.datetime.now)  # Automatically set the field to now when the object is first created

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
            

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'store')  # This will enforce the combination to be unique

    def __str__(self):
        return f"{self.user.username} - {self.store.store_name if self.store else 'No Store Assigned'}"

       
