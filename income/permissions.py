from lib2to3.pytree import Base
from rest_framework.permissions import BasePermission
from authentication.models import CustomUser

class IsOwner(BasePermission):
   def has_object_permission(self, request, view, obj):
       return obj.owner == request.user