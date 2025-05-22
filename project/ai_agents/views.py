from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .agents import EventAnalysisAgent

# Create your views here.

@login_required
def get_recommendations(request):
    """Get personalized event recommendations for the current user."""
    agent = EventAnalysisAgent()
    recommendations = agent.get_user_recommendations(request.user)
    
    context = {
        'recommendations': recommendations
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON for AJAX requests
        return JsonResponse({
            'recommendations': [
                {
                    'id': rec['event'].id,
                    'title': rec['event'].title,
                    'score': rec['score'],
                    'reason': rec['reason']
                }
                for rec in recommendations
            ]
        })
    
    # Return HTML for regular requests
    return render(request, 'ai_agents/recommendations.html', context)

@login_required
def event_analysis(request, event_id):
    """Get AI analysis for a specific event."""
    agent = EventAnalysisAgent()
    analysis = agent.analyze_event_performance(event_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(analysis)
    
    return render(request, 'ai_agents/event_analysis.html', {'analysis': analysis})

@login_required
def event_optimization(request, event_id):
    """Get AI optimization suggestions for an event."""
    agent = EventAnalysisAgent()
    optimization = agent.optimize_event_parameters(event_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(optimization)
    
    return render(request, 'ai_agents/event_optimization.html', {'optimization': optimization})
