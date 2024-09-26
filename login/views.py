from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.cache import cache
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model


class LoginView(APIView):
    permission_classes = (AllowAny,)
    MAX_ATTEMPTS = 5
    BLOCK_TIME = 1 * 60

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Usuário e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)


        lockout_time = cache.get(f'lockout_{username}')
        if lockout_time:
            remaining_time = (lockout_time - timezone.now()).total_seconds()

            if remaining_time > 0:
                return Response({
                    "success": False,
                    "message": "Conta bloqueada. Tente novamente mais tarde.",
                    "remaining_time": int(remaining_time)
                }, status=status.HTTP_403_FORBIDDEN)
            else:
                cache.delete(f'lockout_{username}')

        user = authenticate(username=username, password=password)

        if user is not None:
            cache.delete(f'login_attempts_{username}')
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'token': token.key,
                'username': user.username,
                'message': 'Login realizado com sucesso.'
            })
        else:
            attempts = cache.get(f'login_attempts_{username}', 0)
            attempts += 1
            cache.set(f'login_attempts_{username}', attempts, timeout=self.BLOCK_TIME)

            if attempts >= self.MAX_ATTEMPTS:
                lockout_until = timezone.now() + timedelta(seconds=self.BLOCK_TIME)
                remaining_time = (lockout_until - timezone.now()).total_seconds()
                cache.set(f'lockout_{username}', lockout_until, timeout=self.BLOCK_TIME)


                self.send_unlock_email(username)

                return Response({
                    "success": False,
                    "message": "Muitas tentativas de login falhadas. Conta bloqueada por 10 minutos.",
                    "remaining_time": int(remaining_time)
                }, status=status.HTTP_403_FORBIDDEN)

            return Response({
                'success': False,
                'message': 'Falha no login. Verifique suas credenciais.'
            }, status=status.HTTP_401_UNAUTHORIZED)

    def send_unlock_email(self, username):
        """Envia um e-mail para o usuário com instruções para desbloquear a conta."""
        try:
            user = User.objects.get(username=username)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

            subject = "Conta bloqueada - Instruções de desbloqueio"
            html_message = f"""
            <html>
            <body>
                <p>Olá {user.username},</p>
                <p>Sua conta foi bloqueada devido a várias tentativas de login falhadas. Clique no link abaixo para redefinir sua senha:</p>
                <p><a href="{reset_link}">Redefinir Senha</a></p>
                <p>Se você não fez essas tentativas, por favor, ignore este e-mail.</p>
                <p>Atenciosamente,<br>Sua Equipe</p>
            </body>
            </html>
            """
            plain_message = strip_tags(html_message)

            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        except User.DoesNotExist:
            print(f"Usuário {username} não encontrado. Não foi possível enviar o e-mail.")

