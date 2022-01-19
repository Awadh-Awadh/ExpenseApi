from django.urls import path
from .views import ExpensesListAPIView, ExpensesDetailAPIView



urlpatterns = [
    path("create/", ExpensesListAPIView.as_view(), name='create'),
    path("<int:pk>/", ExpensesDetailAPIView.as_view(), name='detail')

]
