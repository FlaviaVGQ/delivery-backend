from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.cache import cache
from datetime import timedelta
from django.utils import timezone

class LoginView(APIView):
    permission_classes = (AllowAny,)
    MAX_ATTEMPTS = 5  # Número máximo de tentativas permitidas
    BLOCK_TIME = 1 * 60  # Tempo de bloqueio em segundos (10 minutos)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Usuário e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o usuário está bloqueado
        lockout_time = cache.get(f'lockout_{username}')
        if lockout_time:
            # Calcula o tempo restante de bloqueio
            remaining_time = (lockout_time - timezone.now()).total_seconds()

            if remaining_time > 0:
                # Envia o tempo restante em segundos para o front-end
                return Response({
                    "success": False,
                    "message": "Conta bloqueada. Tente novamente mais tarde.",
                    "remaining_time": int(remaining_time)  # Tempo restante em segundos
                }, status=status.HTTP_403_FORBIDDEN)
            else:
                # Remove o bloqueio após o tempo passar
                cache.delete(f'lockout_{username}')

        # Autentica o usuário
        user = authenticate(username=username, password=password)

        if user is not None:
            # Limpa as tentativas após login bem-sucedido
            cache.delete(f'login_attempts_{username}')
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'token': token.key,
                'message': 'Login realizado com sucesso.'
            })
        else:
            # Incrementa o contador de tentativas falhas
            attempts = cache.get(f'login_attempts_{username}', 0)
            attempts += 1
            cache.set(f'login_attempts_{username}', attempts, timeout=self.BLOCK_TIME)

            # Se exceder o número de tentativas, aplica o bloqueio
            if attempts >= self.MAX_ATTEMPTS:
                lockout_until = timezone.now() + timedelta(seconds=self.BLOCK_TIME)
                remaining_time = (lockout_until - timezone.now()).total_seconds()
                cache.set(f'lockout_{username}', lockout_until, timeout=self.BLOCK_TIME)
                return Response({
                    "success": False,
                    "message": "Muitas tentativas de login falhadas. Conta bloqueada por 10 minutos.",
                    "remaining_time": int(remaining_time)  # Tempo restante em segundos
                }, status=status.HTTP_403_FORBIDDEN)
            print(Response)
            return Response({
                'success': False,
                'message': 'Falha no login. Verifique suas credenciais.'
            }, status=status.HTTP_401_UNAUTHORIZED)
