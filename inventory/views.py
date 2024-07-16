"""
Views for the inventory app.
"""

from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Item
from .serializers import ItemSerializer, UserSerializer
from .permissions import IsAdminOrJWTAuthenticated

class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Items.
    Admin users can perform CRUD operations without JWT.
    Regular users can only list items and must be JWT authenticated.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminOrJWTAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new item.
        Only admins can create items without JWT.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Handle updating an existing item.
        Only admins can update items without JWT.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Handle deleting an existing item.
        Only admins can delete items without JWT.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserCreateView(generics.CreateAPIView):
    """
    View for handling user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
