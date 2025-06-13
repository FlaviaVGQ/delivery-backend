from django.urls import path
from .views import OrderReportPDFView

urlpatterns = [
    path('pdf/', OrderReportPDFView.as_view(), name='order_report_pdf'),
]