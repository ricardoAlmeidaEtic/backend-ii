from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Event, EventCategory
from ai_agents.agents import EventAnalysisAgent
from unittest.mock import patch
from datetime import datetime, timedelta

class AIIntegrationTests(APITestCase):
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

    @patch('ai_agents.agents.EventAnalysisAgent.get_user_recommendations')
    def test_get_recommendations(self, mock_recommendations):
        """Test getting AI recommendations for events"""
        mock_recommendations.return_value = [
            {
                'event_id': self.event.id,
                'score': 0.95,
                'reason': 'Based on user preferences'
            }
        ]
        
        url = reverse('event-recommended')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_recommendations.assert_called_once_with(self.user)
        self.assertEqual(len(response.data), 1)

    @patch('ai_agents.agents.EventAnalysisAgent.analyze_event_performance')
    def test_event_analysis(self, mock_analysis):
        """Test getting AI analysis for an event"""
        mock_analysis.return_value = {
            'attendance_rate': 0.85,
            'satisfaction_score': 4.5,
            'engagement_level': 'High',
            'recommendations': ['Consider increasing capacity']
        }
        
        url = reverse('event-analysis', args=[self.event.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_analysis.assert_called_once_with(str(self.event.id))
        self.assertIn('attendance_rate', response.data)
        self.assertIn('recommendations', response.data)

    @patch('ai_agents.agents.EventAnalysisAgent.optimize_event_parameters')
    def test_event_optimization(self, mock_optimization):
        """Test getting AI optimization suggestions"""
        mock_optimization.return_value = {
            'suggested_capacity': 150,
            'ideal_date': (datetime.now() + timedelta(days=14)).isoformat(),
            'price_point': 49.99,
            'marketing_channels': ['Email', 'Social Media']
        }
        
        url = reverse('event-optimization', args=[self.event.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_optimization.assert_called_once_with(str(self.event.id))
        self.assertIn('suggested_capacity', response.data)
        self.assertIn('marketing_channels', response.data)

    def test_unauthorized_ai_access(self):
        """Test that AI endpoints require authentication"""
        # Logout user
        self.client.force_authenticate(user=None)
        
        # Test recommendations endpoint
        url = reverse('event-recommended')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test analysis endpoint
        url = reverse('event-analysis', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test optimization endpoint
        url = reverse('event-optimization', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 