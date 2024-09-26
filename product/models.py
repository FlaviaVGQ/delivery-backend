from django.db import models
from django.contrib.auth.models import User
from category.models import Category  # Importa o modelo Category de outro módulo

class Product(models.Model):
    name = models.CharField(max_length=255)  # Nome do produto
    description = models.TextField()  # Descrição do produto
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço do produto
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')  # Relação com Category
    image = models.ImageField(upload_to='products/')  # Caminho da imagem do produto
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)  # Permitir nulos

    def __str__(self):
        return self.name
