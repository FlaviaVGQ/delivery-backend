from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
import os
from django.conf import settings

class ProductView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('categoryId')
        image = request.FILES.get('image')

        print(name)# Obtém a imagem do request

        # Validação dos dados recebidos
        if not name or not description or not price or not category_id or not image:
            return Response({"error": "Todos os campos são obrigatórios."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Tenta obter a categoria e o usuário
        try:
            user = User.objects.get(id=request.user.id)  # Obtém o usuário autenticado
            category = Category.objects.get(id=category_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Salvar a imagem em um diretório específico
        image_path = os.path.join(settings.MEDIA_ROOT, 'products', image.name)  # Define o caminho da imagem
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Cria e salva o novo produto
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image_path  # Salva o caminho da imagem
        )
        product.save()

        return Response({"message": "Produto criado com sucesso!"}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({"error": "ID de usuário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Busca todos os produtos associados ao usuário
        products = Product.objects.filter(category__user=user)  # Filtra produtos pela categoria do usuário

        # Converte os produtos para um formato que pode ser enviado como JSON
        products_data = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "image": product.image,  # Retorna o caminho da imagem
                "category": product.category.name
            }
            for product in products
        ]
        print(products_data)

        return Response(products_data, status=status.HTTP_200_OK)
