from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email_or_username = request.data.get('emailOrUsername')
        print(email_or_username)

        if not email_or_username:
            return Response({"error": "O e-mail ou nome de usuário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verifica se é um e-mail ou nome de usuário
            if '@' in email_or_username:
                user = User.objects.get(email=email_or_username)
            else:
                user = User.objects.get(username=email_or_username)
        except User.DoesNotExist:
            # Retorna uma mensagem de erro se o e-mail ou nome de usuário não forem encontrados
            return Response({"error": "E-mail ou nome de usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Gera o token e o UID para redefinição de senha
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"  # Ajuste conforme necessário

        # Envia o e-mail de redefinição de senha
        self.send_reset_email(user.email, reset_link)

        # Retorna mensagem de sucesso
        return Response({"message": "E-mail de recuperação enviado com sucesso. Verifique sua caixa de entrada."}, status=status.HTTP_200_OK)

    def send_reset_email(self, email, reset_link):
        subject = "Redefinição de Senha"
        message = f"""
        Olá,

        Você solicitou a redefinição de sua senha. Clique no link abaixo para redefinir sua senha:

        {reset_link}

        Se você não solicitou essa mudança, ignore este e-mail.

        Atenciosamente,
        Delivery Express
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
