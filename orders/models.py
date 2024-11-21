from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=255)  # Nome do cliente
    observation = models.TextField(blank=True, null=True)  # Observação opcional
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total do pedido
    created_at = models.DateTimeField(auto_now_add=True)  # Data do pedido

    def __str__(self):
        return f"Pedido {self.id} - Total: {self.total_price}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} - {self.price}"

