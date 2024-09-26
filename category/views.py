from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


class CategoryView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        category_name = request.data.get('category')
        print(category_name)
        user_id = request.data.get('user_id')

        if not category_name or not user_id:
            return Response({"error": "Categoria e ID de usuário são obrigatórios."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Cria e salva a nova categoria
        category = Category(name=category_name, user=user)
        category.save()

        return Response({"message": "Categoria criada com sucesso!"}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')  # Obtém o user_id dos parâmetros da query string

        if not user_id:
            return Response({"error": "ID de usuário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Busca todas as categorias associadas ao usuário
        categories = Category.objects.filter(user=user)
        print (categories)

        # Converte as categorias para um formato que pode ser enviado como JSON
        categories_data = [{"id": category.id, "name": category.name} for category in categories]
        print(categories_data)

        return Response(categories_data, status=status.HTTP_200_OK)

