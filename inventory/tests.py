"""
Unit tests for the inventory app.
"""

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Item

class UserRegistrationTests(APITestCase):
    """
    Tests for user registration endpoint.
    """
    def test_register_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('user-register')
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class ItemTests(APITestCase):
    """
    Tests for the Item CRUD operations.
    """
    def setUp(self):
        """
        Create a user and admin user.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')

        # Obtain JWT token for regular user
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_token = response.data['access']

        self.item = Item.objects.create(name='Item1', description='Description of Item1', quantity=10)

    def test_list_items_as_user(self):
        """
        Ensure regular users can list items.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('item-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_item_as_admin(self):
        """
        Ensure admin users can create items without JWT.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('item-list')
        data = {
            "name": "Item2",
            "description": "Description of Item2",
            "quantity": 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.get(id=2).name, 'Item2')

    def test_create_item_as_user(self):
        """
        Ensure regular users cannot create items.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('item-list')
        data = {
            "name": "Item2",
            "description": "Description of Item2",
            "quantity": 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item_as_admin(self):
        """
        Ensure admin users can update items without JWT.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('item-detail', args=[self.item.id])
        data = {
            "name": "Updated Item1",
            "description": "Updated description of Item1",
            "quantity": 15
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item1')

    def test_update_item_as_user(self):
        """
        Ensure regular users cannot update items.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('item-detail', args=[self.item.id])
        data = {
            "name": "Updated Item1",
            "description": "Updated description of Item1",
            "quantity": 15
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_item_as_admin(self):
        """
        Ensure admin users can delete items without JWT.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_item_as_user(self):
        """
        Ensure regular users cannot delete items.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
