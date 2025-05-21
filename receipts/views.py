from django.http import JsonResponse
from django.shortcuts import render

from receipts.models import Store
from .generateTrans import collect_and_insert_transactions
from erp.getMeterReading import collectInfoMeterReadingShift
from django.contrib.auth.decorators import login_required



@login_required
def store_list_view(request):
    user = request.user
    if user.is_superuser:
        stores = Store.objects.all()
    else:
        stores = Store.objects.filter(id=user.userprofile.store.id)

    return render(request, 'store_list.html', {'stores': stores})

def collect_transactions_view(request):
    # Example parameters (these can be passed via GET or POST in a real request)
    target_volume = float(request.GET.get('target_volume', 22723.00))  # Default to 1000 if not provided
    target_date_str = request.GET.get('target_date', '2022-09-02')  # Default date
    station_code = int(request.GET.get('station_code', 2009))  # Default station code
    product = request.GET.get('product', 'G92')  # Default product
    shift_no = request.GET.get('shift_no', 1)  # Default product
    
    
    meterInfo=collectInfoMeterReadingShift(station_code, product,target_date_str,shift_no)  # Call the function to collect meter readings

    # Call the function
    inserted_count, collected_volume = collect_and_insert_transactions(
        target_volume=meterInfo['total_qty'],
        target_date_str=target_date_str,
        station_code=station_code,
        meterReading=meterInfo['reading_no'],
        product=product
    )

    # Return a JSON response
    return JsonResponse({
        'inserted_count': inserted_count,
        'collected_volume': collected_volume
    })
# Create your views here.
