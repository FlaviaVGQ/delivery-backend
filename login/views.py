from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def exemplo_view(request):
    data = {
        'mensagem': 'Olá do Django!!',
        'status': 'success'
    }
    return Response(data)

