from receipts.models import Store  
from datetime import datetime, timedelta
from receipts.models import HistoricalData, TransactionsDetails  # Adjust import as needed
from django.db import transaction
from django.db import IntegrityError, DatabaseError
import traceback

# step 2: collect data from the historical data table
# This function collects transactions from the historical data table based on the given parameters. then it inserts them into the TransactionsDetails table.
# It continues to collect transactions until the target volume is reached or exceeded.


def collect_and_insert_transactions(target_volume, target_date_str, station_code, product, meterReading, today_price, shift_No, lastReceiptNumber, shiftCount):
    try:
        #target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        #historical_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        neededDates=get_shift_datetime_range(target_date_str, shift_No, shiftCount)
        target_date = neededDates[0].date()
        historical_date = neededDates[1].date()
        #set target date from above def
        historical_date_minus_3 = historical_date.replace(year=historical_date.year - 0)  # looks like you meant -3?
        shiftTimes= getShiftTimeForStationsBy(shift_No, shiftCount)
        start_time = datetime.strptime(shiftTimes[0], '%H:%M:%S').time()
        end_time = datetime.strptime(shiftTimes[1], '%H:%M:%S').time()
        collected = []
        collected_volume = 0
        days_offset = 0
        checked_dates = set()

        while collected_volume < target_volume:
            try:
                back_date = historical_date_minus_3 + timedelta(days=days_offset)

                if back_date in checked_dates:
                    days_offset = -days_offset if days_offset > 0 else -days_offset + 1
                    continue

                checked_dates.add(back_date)

                rows = HistoricalData.objects.filter(
                    station_code=station_code,
                    product=product,
                    date=back_date,
                    start_date__time__gte=start_time,
                    end_date__time__lte=end_time
                ).order_by('start_date')

                print(f"Rows found for date {back_date}: {len(rows)}")

                for row in rows:
                    collected.append(row)
                    collected_volume += float(row.volume)
                    if collected_volume >= target_volume:
                        break

                if collected_volume >= target_volume:
                    break

                days_offset = -days_offset if days_offset > 0 else -days_offset + 1

            except Exception as e:
                print(f"Error fetching rows for date {back_date}: {e}")
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
                        date=target_date,
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
                store.latest_used_Receipt = latest_generated_receipt
                store.save()
                    

           

        except (IntegrityError, DatabaseError) as db_err:
            print(f"Database error during insert: {db_err}")
            traceback.print_exc()

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()


# call third step to fix excess insertions
    fix_excess_insert(meterReading, target_volume)



# step 3: fix excess insertions
# This function checks if the total volume of inserted transactions exceeds the target volume. If it does, it finds the closest transaction to the excess and deletes it.   
def fix_excess_insert(meterreadingNo, target_volume):
    # Step 1: Get all inserted records matching the filter
    inserted = TransactionsDetails.objects.filter(
        meterreading_no=meterreadingNo
        
    )

    # Step 2: Calculate total inserted volume
    total_volume = sum([float(t.volume) for t in inserted])
    excess = total_volume - float(target_volume)

    if excess <= 0:
        print("No excess to fix.")
        return

    # Step 3: Find the closest transaction to the excess
    closest = None
    closest_diff = None

    for t in inserted:
        diff = abs(float(t.volume) - excess)
        if closest is None or diff < closest_diff:
            closest = t
            closest_diff = diff

    # Optional: only delete if it's close enough (e.g., within ±2)
    if closest and abs(float(closest.volume) - excess) <= 2:
        closest.delete()
        print(f"Deleted transaction with volume {closest.volume} to fix excess.")
    else:
        print(f"No close enough transaction {closest.volume}  found to delete.")
        
        
def split_receipt(latest_receipt_number):
    """
    Splits a receipt number into prefix and numeric part.
    Supports formats like '000201-F0000000123' or '000201-P0000000456'.
    
    Returns:
        (prefix, number_part) -> (str, int)
    """
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

def get_shift_datetime_range(target_date_str, shift_no, shift_count):
    historical_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    shift_times = getShiftTimeForStationsBy(shift_no, shift_count)

    start_time = datetime.strptime(shift_times[0], '%H:%M:%S').time()
    end_time = datetime.strptime(shift_times[1], '%H:%M:%S').time()

    # Combine date and time into datetime
    start_datetime = datetime.combine(historical_date, start_time)

    # If end time is less than start time, it's on the next day
    if end_time <= start_time:
        end_datetime = datetime.combine(historical_date + timedelta(days=1), end_time)
    else:
        end_datetime = datetime.combine(historical_date, end_time)

    return start_datetime, end_datetime
