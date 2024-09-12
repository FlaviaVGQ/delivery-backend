from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json


class ForgotPasswordView(View):
    @csrf_exempt  # Remove CSRF verification for this view
    def post(self, request, *args, **kwargs):
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            email_or_username = data.get('emailOrUsername')

            # Find the user by email or username
            try:
                user = User.objects.get(email=email_or_username) or User.objects.get(username=email_or_username)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Usuário não encontrado.'}, status=400)

            # Send email (this is just a placeholder, customize as needed)
            send_mail(
                'Recuperação de Senha',
                'Instruções para redefinir sua senha.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'E-mail de recuperação enviado com sucesso.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
