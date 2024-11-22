from django.urls import path
from .views import DepositMoneyView, TransactionReportView

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit'),
    path('report/', TransactionReportView.as_view(), name='report'),
]