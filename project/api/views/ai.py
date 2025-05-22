from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from ..models import Event
from ai_agents.agents import EventAnalysisAgent


class EventRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            agent = EventAnalysisAgent()
            recommendations = agent.get_user_recommendations(request.user)
            return Response({
                'recommendations': recommendations
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            agent = EventAnalysisAgent()
            analysis = agent.analyze_event_performance(event_id)
            return Response({
                'analysis': analysis
            })
        except Event.DoesNotExist:
            return Response({
                'error': 'Event not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventOptimizationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            agent = EventAnalysisAgent()
            optimization = agent.optimize_event_parameters(event_id)
            return Response({
                'optimization': optimization
            })
        except Event.DoesNotExist:
            return Response({
                'error': 'Event not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(login_required, name='dispatch')
class EventRecommendationsView(TemplateView):
    template_name = 'ai/recommendations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = EventAnalysisAgent()
        context['recommendations'] = agent.get_user_recommendations(self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class EventAnalysisTemplateView(TemplateView):
    template_name = 'ai/event_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        agent = EventAnalysisAgent()
        
        context['event'] = event
        context['analysis'] = agent.analyze_event_performance(event_id)
        return context


@method_decorator(login_required, name='dispatch')
class EventOptimizationTemplateView(TemplateView):
    template_name = 'ai/event_optimization.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        agent = EventAnalysisAgent()
        
        context['event'] = event
        context['optimization'] = agent.optimize_event_parameters(event_id)
        return context 