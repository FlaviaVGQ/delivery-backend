from django.urls import path
from .views import ResetPasswordView

urlpatterns = [
    path('resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),
]
