from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Expenses
from .serializers import ExpensesSerializer
# Create your views here.


class ExpensesListAPIView(generics.ListCreateAPIView):
    serializer_class = ExpensesSerializer
    permissions_classes= (permissions.IsAuthenticated,)



    def get_queryset(self):
        return Expenses.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)