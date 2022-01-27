from django.urls import path
from .views import ExpenseStarts, IncomeStartsAPI

urlpatterns = [
    path("stats/", ExpenseStarts.as_view(), name='status-chats'),
    path("stats/income", IncomeStartsAPI.as_view(), name='income-stats'),
]
