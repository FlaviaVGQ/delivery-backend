from django.urls import path
from .views import ProductView

urlpatterns = [
    path('addProduct/', ProductView.as_view(), name='product'),
    path('products/', ProductView.as_view(), name='product'),
]
