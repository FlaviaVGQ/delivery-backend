from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewCompanyInfo  # Atualize aqui
from django.contrib.auth.models import User
import json

@csrf_exempt  # Use isso com cautela
def save_company_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Obter dados da requisição
            name = data.get('name')
            opening_hours = data.get('opening_hours', '')  # Campo opcional
            address = data.get('address', '')  # Campo opcional
            contact = data.get('contact', '')  # Campo opcional
            user_id = data.get('user_id')

            # Validar se os campos obrigatórios estão presentes
            if not name:
                return JsonResponse({'error': 'Nome da empresa é obrigatório.'}, status=400)

            if not user_id:
                return JsonResponse({'error': 'ID de usuário é obrigatório.'}, status=400)

            user_id = int(user_id)  # Tentar converter o user_id para um inteiro
            user = User.objects.get(id=user_id)  # Verificar se o usuário existe

            # Tentar encontrar uma instância existente de NewCompanyInfo para o user_id
            company_info, created = NewCompanyInfo.objects.update_or_create(
                user=user,
                defaults={
                    'name': name,
                    'opening_hours': opening_hours,
                    'address': address,
                    'contact': contact,
                }
            )

            if created:
                message = 'Informações da empresa salvas com sucesso!'
            else:
                message = 'Informações da empresa atualizadas com sucesso!'

            return JsonResponse({
                'message': message,
                'data': {
                    'id': company_info.id,
                    'name': company_info.name,
                    'opening_hours': company_info.opening_hours,
                    'address': company_info.address,
                    'contact': company_info.contact,
                    'user_id': company_info.user.id  # Incluindo o ID do usuário na resposta
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos.'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'ID de usuário deve ser um número.'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
