from django.urls import path
from .views import ForgotPasswordView

urlpatterns = {
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
}

