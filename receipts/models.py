from django.db import models

# Create your models here.

class Receipt(models.Model):
    """
    Model to represent a receipt.
    """
    receipt_number = models.CharField(max_length=20, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    branch = models.CharField(max_length=100)

    def __str__(self):
        return f"Receipt {self.receipt_number} - {self.branch}"
