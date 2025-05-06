from decimal import Decimal
from receipts.models import Store  
from datetime import datetime, timedelta
from django.utils import timezone
from receipts.models import HistoricalData, TransactionsDetails  # Adjust import as needed
from django.db import transaction
from django.db import IntegrityError, DatabaseError
import traceback
from django.db.models import Q

# step 2: collect data from the historical data table
# This function collects transactions from the historical data table based on the given parameters. then it inserts them into the TransactionsDetails table.
# It continues to collect transactions until the target volume is reached or exceeded.


def collect_and_insert_transactions(target_volume, target_date_str, station_code, product, meterReading, today_price, shift_No, lastReceiptNumber, shiftCount):
   
        try:
            start_dt, end_dt = get_shift_datetime_range(target_date_str, shift_No, shiftCount)

            # Extract time portion from start_dt and end_dt
            start_time = start_dt.time()
            end_time = end_dt.time()

            if start_time <= end_time:
                # Same-day shift
                time_filter = Q(start_date__time__gte=start_time, start_date__time__lte=end_time)
            else:
                # Overnight shift (e.g., 23:00 to 07:00)
                time_filter = Q(start_date__time__gte=start_time) | Q(start_date__time__lte=end_time)
            collected = []
            collected_volume = 0.0
            offset = 0
            max_lookback = 10  # Safety limit: don't look back forever

            while collected_volume < target_volume and abs(offset) <= max_lookback:
                # Expand the search window
                # date_range_start = start_dt - timedelta(days=offset)
                # date_range_end = end_dt + timedelta(days=offset)
                print(f"{start_dt.strftime('%Y-%m-%d %H:%M:%S')} - {end_dt.strftime('%Y-%m-%d %H:%M:%S')} offset: {time_filter}")

               # Final query
                rows = HistoricalData.objects.filter(
                    station_code=station_code,
                    product=product,
                    start_date__range=(start_dt, end_dt)
                ).filter(time_filter).order_by('start_date')
                

                #print(f"Rows found between {date_range_start} and {date_range_end}: {len(rows)}")

                for row in rows:
                    collected.append(row)
                    collected_volume += float(row.volume)
                    if collected_volume >= target_volume:
                        break

                if collected_volume >= target_volume:
                    break

                # Increment offset to widen the range both backward and forward
                offset += 1

        except Exception as e:
            #print(f"Error during data collection: {e}")
            import traceback
            traceback.print_exc()


        # Insert into TransactionsDetails
        
        try:
            
           
            with transaction.atomic():
               

                # 2. Extract latest receipt number
                prefix, current_receipt_num = split_receipt(lastReceiptNumber)

                # 3. Prepare the details to insert
                details_to_insert = []
                for index, row in enumerate(collected):
                    new_receipt_num = current_receipt_num + index + 1
                    receipt_no = f"{prefix}{str(new_receipt_num).zfill(10)}"  # prefix dynamic


                    detail = TransactionsDetails(
                        station_code=row.station_code,
                        station_name=row.station_name,
                        start_date=row.start_date,
                        end_date=row.end_date,
                        date=start_dt,
                        hour=row.hour,
                        pump_id=row.pump_id,
                        hose_id=row.hose_id,
                        volume=row.volume,
                        ppu=today_price,
                        money=float(today_price) * float(row.volume),
                        grade_id=row.grade_id,
                        product=row.product,
                        meterreading_no=meterReading,
                        shift=shift_No,
                        receiptNo=receipt_no
                    )
                    details_to_insert.append(detail)

                # 4. Bulk insert all at once
                TransactionsDetails.objects.bulk_create(details_to_insert)

                # 5. Update the store with the latest receipt number used
                latest_generated_receipt = f"000201-F{str(current_receipt_num + len(collected)).zfill(10)}"
                updateStoreByLastReceiptNumber(station_code, latest_generated_receipt)
                    

           

        except (IntegrityError, DatabaseError) as db_err:
            #print(f"Database error during insert: {db_err}")
            traceback.print_exc()

        except Exception as e:
            #print(f"Unexpected error: {e}")
            traceback.print_exc()


    # call third step to fix excess insertions
        fix_excess_insert(meterReading, target_volume,start_dt,end_dt,product)



# step 3: fix excess insertions
# This function checks if the total volume of inserted transactions exceeds the target volume. If it does, it finds the closest transaction to the excess and deletes it.   


def fix_excess_insert(meterreadingNo, target_volume,start_date,end_date,strProd):
    # Step 1: Get all existing transactions
    inserted = TransactionsDetails.objects.filter(meterreading_no=meterreadingNo,product=strProd)

    # Step 2: Calculate total inserted volume
    total_volume = sum(Decimal(t.volume) for t in inserted)
    difference = total_volume - Decimal(target_volume)

    if abs(difference) < Decimal("0.01"):
        #print("No significant difference to fix.")
        return

    # Step 3: Insert a compensating transaction (negative or positive)
    TransactionsDetails.objects.create(
        meterreading_no=meterreadingNo,
        volume=-difference,  # Negative if excess, positive if shortage
        start_date=start_date,
        end_date=end_date,
        product=strProd,  # Assuming all products are the same
        station_code=inserted[0].station_code,
        ppu=inserted[0].ppu,  # Assuming all prices are the same
        money=difference*inserted[0].ppu,  # Set to 0 for the adjustment transaction
        date=start_date,
        created_at=timezone.now(),  # or your model’s default datetime field
        is_adjustment=True  # Add this field in your model if needed
    )

    #print(f"Inserted adjustment transaction with volume {-difference} to fix difference.")

        
        
def split_receipt(latest_receipt_number):
    
    try:
        if 'F' in latest_receipt_number:
            parts = latest_receipt_number.split('F')
            prefix = parts[0] + 'F'
            number_part = int(parts[1])
        elif 'P' in latest_receipt_number:
            parts = latest_receipt_number.split('P')
            prefix = parts[0] + 'P'
            number_part = int(parts[1])
        else:
            # fallback: unknown format
            prefix = '000201-F'
            number_part = 0
    except (ValueError, IndexError):
        prefix = '000201-F'
        number_part = 0

    return prefix, number_part

def getShiftTimeForStationsBy(shiftNo,shiftCount):
    """
    Returns the start and end time for a given shift number.
    """
    if shiftCount == 3:
        if shiftNo == 1:
            return "23:00:00", "07:00:00"
        elif shiftNo == 2:
            return "07:00:00", "15:00:00"
        elif shiftNo == 3:
            return "15:00:00", "23:00:00"
        else:
            raise ValueError("Invalid shift number")
    elif shiftCount == 2:
        if shiftNo == 2:
             return "08:00:00", "20:00:00"
        elif shiftNo == 1:
            return "20:00:00", "08:00:00"
        else:
            raise ValueError("Invalid shift number")



from datetime import datetime, timedelta

def get_shift_datetime_range(backDate, shift_no, shift_count):
    """
    Returns the full datetime range for a given shift on a specific date.
    Handles both same-day and overnight shifts (e.g., 23:00 to 07:00).

    Args:
        target_date_str (str): Date string in 'YYYY-MM-DD' format.
        shift_no (int): Shift number.
        shift_count (int): Total number of shifts.

    Returns:
        (datetime, datetime): start_datetime, end_datetime of the shift.
    """
    historical_date = datetime.strptime(backDate, '%Y-%m-%d').date()
    
    # Fetch start and end times for the shift
    shift_times = getShiftTimeForStationsBy(shift_no, shift_count)
    if not shift_times or len(shift_times) != 2:
        raise ValueError("Shift times must contain exactly two time strings: [start_time, end_time]")

    # Parse time strings to time objects
    start_time = datetime.strptime(shift_times[0], '%H:%M:%S').time()
    end_time = datetime.strptime(shift_times[1], '%H:%M:%S').time()

    # Combine date and time into datetime
    start_datetime = datetime.combine(historical_date, start_time)

    # If end time is less than or equal to start, it means the shift crosses to the next day
    if end_time <= start_time:
        end_datetime = datetime.combine(historical_date + timedelta(days=1), end_time)
    else:
        end_datetime = datetime.combine(historical_date, end_time)

    return start_datetime, end_datetime


def updateStoreByLastReceiptNumber(storeID, lastReceiptNumber):
    """
    Updates the store's latest used receipt number.
    """
    try:
        store = Store.objects.get(store_id=storeID)
        store.latest_used_Receipt = lastReceiptNumber
        store.save()
        #print(f"Store {storeID} updated with latest receipt number {lastReceiptNumber}.")
    except Store.DoesNotExist:
        print(f"Store {storeID} does not exist.")
    except Exception as e:
        print(f"Error updating store {storeID}: {e}")
