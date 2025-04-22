import datetime
from django.shortcuts import render
from erp.models import ProductPrice

# Create your views here.
def index(request):
    """
    This view handles the index page of the ERP app.
    It fetches today's prices from the ERP database and renders them in the template.
    """
    # Fetch today's prices from ERP
    today_prices = ProductPrice.objects.using('erp')

    # Example: You can pass the prices to the template context if needed
    context = {
        'today_prices': today_prices,
    }

    return render(request, 'index.html', context)  
