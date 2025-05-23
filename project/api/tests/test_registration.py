from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Event, EventRegistration, EventCategory
from datetime import datetime, timedelta

class EventRegistrationTests(APITestCase):
    def setUp(self):
        # Create test users
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
            capacity=2  # Small capacity to test limits
        )

    def test_register_for_event(self):
        """Test registering for an event"""
        url = reverse('eventregistration-list')
        data = {
            'event': self.event.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(EventRegistration.objects.filter(
            user=self.user,
            event=self.event
        ).exists())

    def test_register_full_event(self):
        """Test registering for a full event"""
        # Create two registrations to fill the event
        EventRegistration.objects.create(user=self.user, event=self.event)
        
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        EventRegistration.objects.create(user=other_user, event=self.event)
        
        # Try to register a third user
        third_user = User.objects.create_user(
            username='thirduser',
            password='testpass123'
        )
        self.client.force_authenticate(user=third_user)
        
        url = reverse('eventregistration-list')
        data = {
            'event': self.event.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('capacity', response.data['error'].lower())

    def test_mark_attendance(self):
        """Test marking attendance for an event"""
        registration = EventRegistration.objects.create(
            user=self.user,
            event=self.event
        )
        
        url = reverse('eventregistration-mark-attended', args=[registration.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        registration.refresh_from_db()
        self.assertTrue(registration.attended)

    def test_list_user_registrations(self):
        """Test listing user's event registrations"""
        # Create a registration
        EventRegistration.objects.create(user=self.user, event=self.event)
        
        url = reverse('eventregistration-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.event.id) 