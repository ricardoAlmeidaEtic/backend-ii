from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_with_invalid_data(self):
        """Test user registration with invalid data"""
        # Test with mismatched passwords
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'wrongpass'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with existing username
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test user login"""
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Test login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_with_invalid_credentials(self):
        """Test user login with invalid credentials"""
        login_data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_access(self):
        """Test accessing protected endpoints with and without authentication"""
        # Create a user and get their token
        user = User.objects.create_user(username='testuser', password='testpass123')
        token = Token.objects.create(user=user)
        
        # Try accessing protected endpoint without authentication
        url = reverse('eventregistration-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Try accessing with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        """Test user logout"""
        # Create and login user
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=user)
        
        # Test logout
        logout_url = reverse('logout')
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify can't access protected endpoint after logout
        url = reverse('eventregistration-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 