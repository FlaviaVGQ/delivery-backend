from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrderList, OrderItem
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class OrderView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"error": "O campo 'user_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuário inválido."}, status=status.HTTP_400_BAD_REQUEST)

            if isinstance(request.data.get('address'), dict):
                address = request.data['address']
                request.data[
                    'address'] = f"{address.get('street', '')}, {address.get('number', '')} - {address.get('complement', '')}, {address.get('district', '')}, {address.get('city', '')} - {address.get('state', '')}"

            order = OrderList.objects.create(
                user=user,
                customer_name=request.data['customer_name'],
                address=request.data['address'],
                phone=request.data['phone'],
                observation=request.data.get('observation', ''),
                total_price=request.data['total_price'],
                payment_method=request.data['payment_method'],
            )

            for item in request.data.get('items', []):
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            return Response({"message": "Pedido criado com sucesso!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Erro ao criar pedido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, order_id=None):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({"error": "O campo 'user_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if order_id:
            try:
                order = OrderList.objects.get(id=order_id, user=user)
                order_data = {
                    "id": order.id,
                    "customer_name": order.customer_name,
                    "address": order.address,
                    "phone": order.phone,
                    "observation": order.observation,
                    "total_price": str(order.total_price),
                    "payment_method": order.payment_method,
                    "created_at": order.created_at,
                    "items": [
                        {
                            "product_name": item.product_name,
                            "quantity": item.quantity,
                            "price": str(item.price)
                        } for item in order.items.all()
                    ]
                }
                return Response(order_data, status=status.HTTP_200_OK)
            except OrderList.DoesNotExist:
                return Response({"error": "Pedido não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = OrderList.objects.filter(user=user)
            order_list = [
                {
                    "id": order.id,
                    "customer_name": order.customer_name,
                    "address": order.address,
                    "phone": order.phone,
                    "observation": order.observation,
                    "total_price": str(order.total_price),
                    "payment_method": order.payment_method,
                    "created_at": order.created_at,
                    "items": [
                        {
                            "product_name": item.product_name,
                            "quantity": item.quantity,
                            "price": str(item.price)
                        }
                        for item in order.items.all()
                    ]
                }
                for order in orders
            ]

            return Response(order_list, status=status.HTTP_200_OK)

    def delete(self, request, order_id=None):
        try:
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"error": "O campo 'user_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            try:
                order = OrderList.objects.get(id=order_id, user=user)
                order.delete()
                return Response({"message": "Pedido excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
            except OrderList.DoesNotExist:
                return Response({"error": "Pedido não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"Erro ao excluir pedido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)