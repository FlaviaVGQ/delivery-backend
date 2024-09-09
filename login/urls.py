from django.urls import path
from .views import exemplo_view

urlpatterns = [
    path('api/exemplo/', exemplo_view, name='exemplo'),
]
