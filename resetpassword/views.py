from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

class ResetPasswordView(View):
    @csrf_exempt
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                password = request.POST.get('password')
                if password:
                    user.set_password(password)
                    user.save()
                    return JsonResponse({'status': 'success', 'message': 'Senha redefinida com sucesso.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Senha não fornecida.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Token inválido ou expirado.'})
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Token inválido ou expirado.'})
