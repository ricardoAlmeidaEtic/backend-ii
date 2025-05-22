from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventViewSet,
    EventRegistrationViewSet,
    EventCategoryViewSet,
    EventFeedbackViewSet
)

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'registrations', EventRegistrationViewSet)
router.register(r'categories', EventCategoryViewSet)
router.register(r'feedback', EventFeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Template URLs
    path('events/', EventViewSet.as_view({'get': 'list'}), name='event-list'),
    path('events/<int:pk>/', EventViewSet.as_view({'get': 'retrieve'}), name='event-detail'),
    path('events/create/', EventViewSet.as_view({'get': 'create', 'post': 'create'}), name='event-create'),
    path('events/<int:pk>/register/', EventRegistrationViewSet.as_view({'post': 'create'}), name='event-registration'),
] 