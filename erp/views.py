import datetime
from django.shortcuts import render
from erp.models import MeterReading, MeterReadingLine
from receipts.models import TransactionsDetails
from django.db.models import Sum

from .getMeterReading import collectInfoMeterReadingShift

# Create your views here.
def index(request):
   
    passwing_work_date ='2022-09-02' #datetime.date.today()  
    filtered_readings_today = MeterReading.objects.using('erp').filter(store_no='2001', status=2, work_date=passwing_work_date).values('reading_no','shift_no').distinct()
   
    #loop in filtered_readings_today to get the reading_no and products in it and pass it to the collectInfoMeterReadingShift function
    
    for reading in filtered_readings_today:
        
        reading_no = reading['reading_no']
        shiftNumber = reading['shift_no']            

        productsInMeterReading = (
            MeterReadingLine.objects
            .filter(reading_no=reading_no)
            .values('fuel_item_type', 'price')
            .annotate(TotalVolume=Sum('qty'))
        )

         
        for meterline in productsInMeterReading:
            #get the product name
            product = meterline['fuel_item_type']
            price= meterline['price']
            totalVolume= meterline['TotalVolume']
            #check if this reading_no is exist in transactiondetails table
            isexist = TransactionsDetails.objects.filter(meterreading_no=reading_no,product=product).values('meterreading_no').distinct()
            
            #if not exist then call the collectInfoMeterReadingShift function
            if not isexist:               
                collectInfoMeterReadingShift('2001', product, price,totalVolume,passwing_work_date, reading_no,shiftNumber)
        
      

    # Example: You can pass the prices to the template context if needed
    context = {
        'filtered_readings': filtered_readings_today,
    }
    
    #collectInfoMeterReadingShift('2001','GO','2022-09-02','1')

    return render(request, 'index.html', context)  

