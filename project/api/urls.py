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
] 