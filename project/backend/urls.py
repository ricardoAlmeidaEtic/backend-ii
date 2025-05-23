"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from api.views import (
    EventViewSet,
    EventRegistrationViewSet,
    EventCategoryViewSet,
    EventFeedbackViewSet,
    RegisterView
)
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer

# Create a router and register our viewsets with it
router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'registrations', EventRegistrationViewSet)
router.register(r'categories', EventCategoryViewSet)
router.register(r'feedback', EventFeedbackViewSet)

# Web views with HTML renderer only
web_event_list = EventViewSet.as_view({
    'get': 'list',
}, renderer_classes=[TemplateHTMLRenderer])

web_event_detail = EventViewSet.as_view({
    'get': 'retrieve',
}, renderer_classes=[TemplateHTMLRenderer])

# The URL patterns
urlpatterns = [
    # Root URL redirect to events
    path('', RedirectView.as_view(url='/events/', permanent=False)),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API URLs - JSON endpoints
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('ai/', include('ai_agents.urls')),
    
    # Frontend URLs
    path('', include('frontend.urls')),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
