from rest_framework.views import APIView  # Adicionando a importação de APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem  # Certifique-se de importar o OrderItem
from .serializers import OrderSerializer

@api_view(['POST'])
def create_order(request):
    data = request.data
    order = Order.objects.create(
        customer_name=data.get('customer_name', 'Anônimo'),
        observation=data.get('observation', ''),
        total_price=data.get('total_price', 0)
    )
    for item in data.get('items', []):
        OrderItem.objects.create(
            order=order,
            product_name=item['name'],
            quantity=item['quantity'],
            price=item['price']
        )
    return Response({"message": "Pedido criado com sucesso!", "order_id": order.id})

@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all().values()
    return Response(list(orders))

class OrderListView(APIView):  # A classe agora está usando APIView corretamente
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
