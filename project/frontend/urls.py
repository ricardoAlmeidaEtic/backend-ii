from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/register/', views.event_register, name='event_register'),
    path('events/<int:pk>/update/', views.event_update, name='event_update'),
    path('my-events/', views.my_events, name='my_events'),
    path('events/recommended/', views.event_recommended, name='event_recommended'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] 