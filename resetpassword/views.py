import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

User = get_user_model()


class ResetPasswordView(View):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            # Verifique o corpo da requisição
            body = json.loads(request.body)
            print("Corpo da requisição:", body)

            # Obter o nome de usuário e a nova senha do corpo da requisição
            username = body.get('username')
            password = body.get('password')
            print(f"Username: {username}, Password: {password}")

            if not username or not password:
                return JsonResponse({'status': 'error', 'message': 'Nome de usuário ou senha não fornecidos.'})

            # Buscar o usuário pelo nome de usuário
            user = User.objects.get(username=username)

            # Alterar a senha
            user.set_password(password)
            user.save()

            return JsonResponse({'status': 'success', 'message': 'Senha redefinida com sucesso.'})

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Erro ao decodificar JSON.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
