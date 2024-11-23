from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewCompanyInfo
from django.contrib.auth.models import User
import json
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings


@csrf_exempt
def save_company_info(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES.get('image', None)
            print(image_file)


            data = request.POST
            name = data.get('name')
            opening_hours = data.get('opening_hours', '')
            address = data.get('address', '')
            contact = data.get('contact', '')
            description = data.get('description', '')
            user_id = data.get('user_id')


            if not name:
                return JsonResponse({'error': 'Nome da empresa é obrigatório.'}, status=400)

            if not user_id:
                return JsonResponse({'error': 'ID de usuário é obrigatório.'}, status=400)

            user = User.objects.get(id=int(user_id))


            company_info, created = NewCompanyInfo.objects.get_or_create(user=user)


            company_info.name = name
            company_info.opening_hours = opening_hours
            company_info.address = address
            company_info.contact = contact
            company_info.description = description


            if image_file and image_file.name != "None":

                user_logo_directory = os.path.join('logoRestaurante', str(user.id))
                logo_directory_path = os.path.join(settings.MEDIA_ROOT, user_logo_directory)
                os.makedirs(logo_directory_path, exist_ok=True)


                fs = FileSystemStorage(location=logo_directory_path)
                filename = fs.save(image_file.name, image_file)
                image_path = os.path.join(user_logo_directory, filename)


                company_info.image = image_path


            company_info.save()

            return JsonResponse({
                'message': 'Informações da empresa salvas com sucesso!',
                'data': {
                    'id': company_info.id,
                    'name': company_info.name,
                    'opening_hours': company_info.opening_hours,
                    'address': company_info.address,
                    'contact': company_info.contact,
                    'description': company_info.description,
                    'user_id': company_info.user.id,
                    'image': company_info.image.url if company_info.image else None
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


from django.http import FileResponse
import base64

@csrf_exempt
def getCompany(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')

            if not user_id:
                return JsonResponse({'error': 'ID de usuário é obrigatório.'}, status=400)

            user = User.objects.get(id=user_id)
            company_info = NewCompanyInfo.objects.get(user=user)


            image_base64 = None
            if company_info.image:
                with open(company_info.image.path, 'rb') as img_file:
                    image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            return JsonResponse({
                'data': {
                    'id': company_info.id,
                    'name': company_info.name,
                    'opening_hours': company_info.opening_hours,
                    'address': company_info.address,
                    'contact': company_info.contact,
                    'description': company_info.description,
                    'user_id': company_info.user.id,
                    'image': image_base64
                }
            }, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)
        except NewCompanyInfo.DoesNotExist:
            return JsonResponse({'error': 'Informações da empresa não encontradas.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
