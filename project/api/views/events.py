from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from ..models import Event, EventRegistration, EventCategory, EventFeedback
from ..serializers import (
    EventSerializer, 
    EventRegistrationSerializer,
    EventCategorySerializer,
    EventFeedbackSerializer
)
from ai_agents.agents import EventAnalysisAgent
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = 'events/list.html'  # Default template
    detail_template_name = 'events/detail.html'  # Template for detail view

    def get_template_names(self):
        if self.action == 'retrieve':
            return [self.detail_template_name]
        return [self.template_name]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # If HTML request
        if isinstance(request.accepted_renderer, TemplateHTMLRenderer):
            # Get AI recommendations if user is authenticated
            recommendations = []
            if request.user.is_authenticated:
                agent = EventAnalysisAgent()
                recommendations = agent.get_user_recommendations(request.user)
            
            return Response({
                'events': queryset,
                'recommendations': recommendations,
                'user': request.user
            })
        
        # API response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()
        
        # If HTML request
        if isinstance(request.accepted_renderer, TemplateHTMLRenderer):
            # Get AI analysis and optimization
            agent = EventAnalysisAgent()
            analysis = agent.analyze_event_performance(event.id)
            optimization = agent.optimize_event_parameters(event.id)
            
            # Check if user is registered
            is_registered = False
            if request.user.is_authenticated:
                is_registered = EventRegistration.objects.filter(
                    event=event,
                    user=request.user
                ).exists()
            
            return Response({
                'event': event,
                'analysis': analysis,
                'optimization': optimization,
                'is_registered': is_registered,
                'user': request.user
            })
        
        # API response
        serializer = self.get_serializer(event)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        agent = EventAnalysisAgent()
        recommendations = agent.get_user_recommendations(request.user)
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def analysis(self, request, pk=None):
        agent = EventAnalysisAgent()
        analysis_results = agent.analyze_event_performance(pk)
        return Response(analysis_results)

    @action(detail=True, methods=['get'])
    def optimization(self, request, pk=None):
        agent = EventAnalysisAgent()
        optimization_results = agent.optimize_event_parameters(pk)
        return Response(optimization_results)


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event = get_object_or_404(Event, id=self.request.data.get('event'))
        if event.registrations.count() >= event.capacity:
            return Response(
                {'error': 'Event is at full capacity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_attended(self, request, pk=None):
        registration = self.get_object()
        registration.attended = True
        registration.save()
        return Response({'status': 'attendance marked'})


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EventFeedbackViewSet(viewsets.ModelViewSet):
    queryset = EventFeedback.objects.all()
    serializer_class = EventFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 