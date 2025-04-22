from django.db import models

class ProductPrice(models.Model):
    product_id = models.IntegerField()
    branch_id = models.IntegerField()
    price_per_liter = models.DecimalField(max_digits=8, decimal_places=3)
    timestamp = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'ProductPrices'

