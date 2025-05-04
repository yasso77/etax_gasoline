
from erp.models import MeterReading, MeterReadingLine
from django.db.models import Sum
from receipts.generateTrans import collect_and_insert_transactions

# STEP 1: Import meter reading data from the ERP database
# This function collects meter reading data for a specific store, fuel type, date, and shift number.
def collectInfoMeterReadingShift(storeID,fueltype,price,totalVolume,date,reading_no,shiftNo,lastReceiptNumber,shiftCount):
        
    collect_and_insert_transactions(
            target_volume=totalVolume,
            target_date_str=date,
            station_code=storeID,
            meterReading=reading_no,
            product=fueltype,
            today_price=price,
            shift_No=shiftNo,
            lastReceiptNumber=lastReceiptNumber,
            shiftCount=shiftCount
        )
       