from celery import shared_task
from django.utils import timezone
from .models import Receipt
from .utils import generate_receipts_for_shift

@shared_task
def generate_shift_receipts():
    """
    Background task to generate receipts for current shifts per branch.
    """
    current_time = timezone.now()
    # Add logic to loop through each branch and fetch the current shift
    # For each, call a utility function to generate receipts based on past data
    generate_receipts_for_shift(current_time)
