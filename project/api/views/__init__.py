from .events import (
    EventViewSet,
    EventRegistrationViewSet,
    EventCategoryViewSet,
    EventFeedbackViewSet
)
from .auth import RegisterView
from .ai import (
    EventRecommendationView,
    EventAnalysisView,
    EventOptimizationView,
    EventRecommendationsView,
    EventAnalysisTemplateView,
    EventOptimizationTemplateView
)

__all__ = [
    'EventViewSet',
    'EventRegistrationViewSet',
    'EventCategoryViewSet',
    'EventFeedbackViewSet',
    'RegisterView',
    'EventRecommendationView',
    'EventAnalysisView',
    'EventOptimizationView',
    'EventRecommendationsView',
    'EventAnalysisTemplateView',
    'EventOptimizationTemplateView'
] 