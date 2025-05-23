from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Event, EventCategory
from datetime import datetime, timedelta

class EventTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test category
        self.category = EventCategory.objects.create(name='Test Category')
        
        # Create test event
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=datetime.now() + timedelta(days=7),
            location='Test Location',
            organizer=self.user,
            category=self.category,
            capacity=100
        )

    def test_create_event(self):
        """Test creating a new event"""
        url = reverse('event-list')
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'date': (datetime.now() + timedelta(days=14)).isoformat(),
            'location': 'New Location',
            'category': self.category.id,
            'capacity': 50
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Event.objects.get(title='New Event').organizer, self.user)

    def test_list_events(self):
        """Test listing all events"""
        url = reverse('event-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Event')

    def test_retrieve_event(self):
        """Test retrieving a specific event"""
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')

    def test_update_event(self):
        """Test updating an event"""
        url = reverse('event-detail', args=[self.event.id])
        data = {
            'title': 'Updated Event',
            'description': self.event.description,
            'date': self.event.date.isoformat(),
            'location': self.event.location,
            'category': self.category.id,
            'capacity': self.event.capacity
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(id=self.event.id).title, 'Updated Event')

    def test_delete_event(self):
        """Test deleting an event"""
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0) 