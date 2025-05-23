from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models import Event, EventRegistration
from .forms import EventForm
from django.http import JsonResponse
from django.utils import timezone
from ai_agents.agents import EventAnalysisAgent


def event_list(request):
    events = Event.objects.all().order_by('-start_date')
    return render(request, 'events/list.html', {'events': events})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = EventRegistration.objects.filter(
        event=event,
        user=request.user
    ).exists()
    
    # Calculate progress percentage
    if event.capacity > 0:
        progress = int((event.registrations.count() / event.capacity) * 100)
    else:
        progress = 0
    
    return render(request, 'events/detail.html', {
        'event': event,
        'is_registered': is_registered,
        'progress': progress
    })


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/create.html', {'form': form})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Check if the user is the organizer
    if event.organizer != request.user:
        messages.error(request, 'You can only edit events you organize.')
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/update.html', {'form': form, 'event': event})


@login_required
def my_events(request):
    organized_events = Event.objects.filter(organizer=request.user)
    registered_events = Event.objects.filter(
        registrations__user=request.user
    )
    
    return render(request, 'events/my_events.html', {
        'organized_events': organized_events,
        'registered_events': registered_events
    })


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if event.is_full:
        messages.error(request, 'This event is already full.')
        return redirect('event_detail', pk=pk)
    
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('event_detail', pk=pk)
    
    EventRegistration.objects.create(
        event=event,
        user=request.user,
        status='confirmed'
    )
    
    messages.success(request, 'Successfully registered for the event!')
    return redirect('event_detail', pk=pk)


@login_required
def event_recommended(request):
    """Get personalized event recommendations for the current user using AI."""
    try:
        # Get user's registered events for context
        user_registered_events = Event.objects.filter(
            registrations__user=request.user
        ).values('title', 'description', 'category')
        
        # Create context for AI recommendation
        user_context = {
            'registered_events': list(user_registered_events),
            'username': request.user.username,
            'interests': [event['category'] for event in user_registered_events if event.get('category')]
        }
        
        # Get AI recommendations
        agent = EventAnalysisAgent()
        ai_recommendations = agent.get_recommendations(user_context)
        
        # Get upcoming events that match AI recommendations
        upcoming_events = Event.objects.filter(
            start_date__gte=timezone.now()
        ).order_by('start_date')
        
        # Filter and sort events based on AI recommendations
        recommended_events = []
        for event in upcoming_events:
            if len(recommended_events) >= 5:  # Limit to 5 recommendations
                break
            # Skip events user is already registered for
            if EventRegistration.objects.filter(event=event, user=request.user).exists():
                continue
            recommended_events.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'start_date': event.start_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse(recommended_events, safe=False)
        
    except Exception as e:
        # Fallback to basic recommendations if AI fails
        upcoming_events = Event.objects.filter(
            start_date__gte=timezone.now()
        ).exclude(
            registrations__user=request.user
        ).order_by('start_date')[:5]
        
        recommendations = [{
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_date': event.start_date.strftime('%Y-%m-%d %H:%M:%S')
        } for event in upcoming_events]
        
        return JsonResponse(recommendations, safe=False)
