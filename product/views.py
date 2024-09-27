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
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('categoryId')
        user_id = request.data.get('userId')
        image = request.FILES.get('image')

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)


        images_dir = os.path.join(settings.MEDIA_ROOT, 'ImagensdosProdutos')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        if image:
            image_path = os.path.join(images_dir, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            image_url = f'{settings.MEDIA_URL}ImagensdosProdutos/{image.name}'
        else:
            image_url = None


        try:
            product = Product(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image_url,
                user=user
            )
            product.save()
            return Response({"message": "Produto adicionado com sucesso."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.query_params.get('user_id')
        products = Product.objects.filter(user=user)
        print(products)


        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "category": product.category.name,
                "image": product.image.url if product.image else None

            }
            for product in products

        ]

        return Response(product_list, status=status.HTTP_200_OK)
