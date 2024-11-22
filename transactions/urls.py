from django.urls import path
from .views import DepositMoneyView, TransactionReportView, WithdrawMoneyView

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit'),
    path('report/', TransactionReportView.as_view(), name='report'),
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw'),
]