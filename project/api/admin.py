from django.contrib import admin
from .models import Event, EventRegistration, EventCategory, EventFeedback


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'capacity', 'organizer', 'is_active')
    list_filter = ('is_active', 'start_date', 'location')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_date'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'registration_date', 'attended')
    list_filter = ('status', 'attended', 'registration_date')
    search_fields = ('event__title', 'user__username')
    date_hierarchy = 'registration_date'


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('event__title', 'user__username', 'comment')
    date_hierarchy = 'created_at'
