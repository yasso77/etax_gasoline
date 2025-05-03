# tasks.py
from celery import shared_task

from receipts.models import Store

@shared_task
def run_my_view_task():
    try:
        from erp.views import runMeterReading  # Import here to avoid circular import issues
        store = Store.objects.get(store_id=2001)
        passwing_work_date ='2022-09-07' #datetime.date.today()  
        response = runMeterReading(passwing_work_date, store.store_id, store.latest_used_Receipt, store.shiftcount) 
        #print("=== TASK STARTED: DATE IS ", passwing_work_date, "===")
        return response
    except Exception as e:
        print(f"Error in running index view: {e}")
        return str(e)
