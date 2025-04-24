from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='erp_index'),
    path('collect-transactions/', views.collect_transactions_view, name='collect_transactions'),
]
