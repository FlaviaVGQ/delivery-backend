from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def exemplo_view(request):
    data = {
        'mensagem': 'Delivery!!',
        'status': 'success'
    }
    return Response(data)

