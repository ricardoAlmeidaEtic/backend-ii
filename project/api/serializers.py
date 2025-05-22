from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventRegistration, EventCategory, EventFeedback


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'description']


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    categories = EventCategorySerializer(many=True, read_only=True)
    registration_count = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'location', 'capacity', 'organizer', 'categories',
            'registration_count', 'is_full', 'created_at', 'updated_at',
            'is_active'
        ]

    def get_registration_count(self, obj):
        return obj.registrations.count()

    def get_is_full(self, obj):
        return obj.registrations.count() >= obj.capacity


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EventRegistration
        fields = [
            'id', 'event', 'event_id', 'user', 'status',
            'registration_date', 'attended'
        ]
        read_only_fields = ['registration_date', 'attended']

    def validate_event_id(self, value):
        try:
            event = Event.objects.get(id=value)
            if event.registrations.count() >= event.capacity:
                raise serializers.ValidationError("Event is at full capacity")
            return value
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event does not exist")


class EventFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EventFeedback
        fields = ['id', 'event', 'event_id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

    def validate_event_id(self, value):
        try:
            event = Event.objects.get(id=value)
            # Check if user has attended the event
            if not EventRegistration.objects.filter(
                event=event,
                user=self.context['request'].user,
                attended=True
            ).exists():
                raise serializers.ValidationError(
                    "You can only provide feedback for events you have attended"
                )
            return value
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event does not exist")