from django.db import models
from inventario.models import Producto

class Order(models.Model):
    order_date = models.DateField(blank=False, null=False)

    def __str__(self):
        return f"Order #{self.pk} - Date:{self.order_date}"

class OrderDetails(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)