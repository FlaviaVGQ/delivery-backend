from django.urls import path
from .views import ResetPasswordView

urlpatterns = [
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
]

