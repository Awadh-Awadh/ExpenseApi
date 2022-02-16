from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import Income

from .serializers import IncomeSerializer
from .permissions import IsOwner



class IncomeAPIView(generics.ListCreateAPIView):

  serializer_class = IncomeSerializer
  permission_classes = (permissions.IsAuthenticated, IsOwner)
  query_set = Income.objects.all()

  """
   perform_create(self, serializer) - Called by CreateModelMixin when saving a new object instance.
   
  """
  def perform_create(self, serializer):
      return serializer.save(owner=self.request.user)

  def get_queryset(self):
      return self.query_set.filter(owner=self.request.user)



class IncomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer


    '''
    Isowner permission class ensures that only the user that created has the right to edit
    
    '''
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    query_set = Income.objects.all()
    lookup_fields = "pk"

    def get_queryset(self):
        return self.query_set.filter(owner=self.request.user)