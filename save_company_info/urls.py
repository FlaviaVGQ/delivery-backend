from django.urls import path
from .views import save_company_info

urlpatterns = [
    path('company-info/', save_company_info, name='save_company_info'),
]