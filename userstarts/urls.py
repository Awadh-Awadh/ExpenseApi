from django.urls import path
from .views import ExpenseStarts

urlpatterns = [
    path("stats/", ExpenseStarts.as_view(), name='status-chats')
]
