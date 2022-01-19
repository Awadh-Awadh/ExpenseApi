from math import perm
from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Expenses
from .serializers import ExpensesSerializer
from .permissions import IsOwner
# Create your views here.


class ExpensesListAPIView(generics.ListCreateAPIView):
    serializer_class = ExpensesSerializer
    permission_classes= (permissions.IsAuthenticated,)



    def get_queryset(self):
        return Expenses.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)



class ExpensesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ExpensesSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)
    lookup_fields = ["pk"]

    def get_queryset(self):
        return Expenses.objects.all().filter(owner=self.request.user)