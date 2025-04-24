
from erp.models import MeterReading, MeterReadingLine
from django.db.models import Sum
from receipts.generateTrans import collect_and_insert_transactions

# STEP 1: Import meter reading data from the ERP database
# This function collects meter reading data for a specific store, fuel type, date, and shift number.
def collectInfoMeterReadingShift(storeID,fueltype,date,shiftNo):
   
    meterReading=MeterReading.objects.using('erp').filter(store_no=storeID,work_date=date, status=2,shift_no=shiftNo).values('reading_no').distinct()
    
    # Check if meterReading is empty
    if not meterReading:
        print("No meter readings found for the given criteria.")
        return 
    else:
    # Example query
        total_qty = MeterReadingLine.objects.using('erp').filter(            
            reading_no=meterReading[0]['reading_no'],
            fuel_item_type=fueltype,
            calibration_qty=0
        ).aggregate(total_qty=Sum('qty'))

        # Retrieve price separately
        price = MeterReadingLine.objects.using('erp').filter(
            reading_no=meterReading[0]['reading_no'],
            fuel_item_type=fueltype,
            calibration_qty=0
        ).values_list('price', flat=True).first()

        # Output results
        
        #call setp 2 to insert data into the database
        
        collect_and_insert_transactions(
            target_volume=total_qty['total_qty'],
            target_date_str=date,
            station_code=storeID,
            meterReading=meterReading[0]['reading_no'],
            product=fueltype,
            today_price=price,
            shift_No=shiftNo
        )
        # return {
        #     'total_qty': total_qty['total_qty'] if total_qty['total_qty'] else 0,
        #     'price': price if price else 0,            
        #     'reading_no': meterReading[0]['reading_no']
        # }