from django.urls import path
from .views import OrderView

urlpatterns = [
    path('orders/', OrderView.as_view(), name='order-list-create'),
    path('get/orders/', OrderView.as_view(), name='get-order-list'),
    path('orders/<int:order_id>/', OrderView.as_view(), name='order-detail'),

]
