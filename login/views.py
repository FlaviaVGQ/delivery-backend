from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import status

class LoginView(APIView):

    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')


        if not username or not password:
            return Response({"error": "Usuário e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'token': token.key,
                'message': 'Login realizado com sucesso.'
            })
        else:
            return Response({
                'success': False,
                'message': 'Falha no login. Verifique suas credenciais.'
            }, status=status.HTTP_401_UNAUTHORIZED)
