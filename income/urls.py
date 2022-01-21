from django.urls import path
from . import views


app_name="income"
urlpatterns = [
    path("", views.IncomeAPIView.as_view(), name='income'),
    path("<int:pk>", views.IncomeDetailAPIView.as_view(), name='detail'),


]
