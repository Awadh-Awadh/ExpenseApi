from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import Income

from .serializers import IncomeSerializer
from .permissions import IsOwner



class IncomeAPIView(generics.ListCreateAPIView):

  serializer_classes = IncomeSerializer
  permission_classes = (permissions.IsAuthenticated,)
  query_set = Income.objects.all()


  def perform_create(self, serializer):
      return Income.objects.all().filter(owner=self.request.user)

  def get_queryset(self):
      return self.query_set.filter(owner=self.request.user)
