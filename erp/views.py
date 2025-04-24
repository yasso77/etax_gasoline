import datetime
from django.shortcuts import render
from erp.models import MeterReading

from .getMeterReading import collectInfoMeterReadingShift

# Create your views here.
def index(request):
   
    # Fetch today's prices from ERP
    filtered_readings = MeterReading.objects.using('erp').filter(store_no='2001', status=2)
    
    #calcQty(request)  # Call the calcQty function to perform calculations

    # Example: You can pass the prices to the template context if needed
    context = {
        'filtered_readings': filtered_readings,
    }
    
    collectInfoMeterReadingShift('2001','G92','2022-09-02','1')

    return render(request, 'index.html', context)  

