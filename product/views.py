import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from category.models import Category
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.conf import settings

class ProductView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # Obter dados do request
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('categoryId')
        user_id = request.data.get('userId')

        # Capturar a imagem do request
        image = request.FILES.get('image')

        # Validação da Categoria
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Validação do Usuário
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar se a pasta existe, caso contrário, criar
        images_dir = os.path.join(settings.BASE_DIR, 'ImagensdosProdutos')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Salvar a imagem na pasta especificada
        if image:
            image_path = os.path.join(images_dir, image.name)  # Caminho completo da imagem
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            image_url = f'ImagensdosProdutos/{image.name}'  # Caminho relativo a ser salvo no banco de dados
        else:
            image_url = None  # Ou você pode definir um valor padrão

        # Criar o Produto
        try:
            product = Product(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image_url,  # Armazenar o caminho relativo da imagem
                user=user
            )
            product.save()
            return Response({"message": "Produto adicionado com sucesso."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.query_params.get('user_id')  # Obtém o user_id dos parâmetros da query string
        print(f"User ID: {user}")

        # Buscar todos os produtos do usuário
        products = Product.objects.filter(user=user)

        # Adiciona um print para listar todos os produtos encontrados
        print("Produtos encontrados:")
        for product in products:
            print(f"ID: {product.id}, Nome: {product.name}, Descrição: {product.description}, Preço: {product.price}")

        # Criar uma lista de dicionários com os produtos
        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),  # Converte Decimal para string
                "category": product.category.name,
                "image": product.image.url if product.image else None  # Obtém a URL da imagem se existir
            }
            for product in products
        ]

        return Response(product_list, status=status.HTTP_200_OK)
