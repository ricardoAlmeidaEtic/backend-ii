from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from typing import List, Dict, Any, Optional
from api.models import Event, EventRegistration, EventFeedback, EventCategory
from django.utils import timezone
from django.db import models
from langchain_community.llms import Ollama
from pydantic import Field, ConfigDict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

class UserPreferencesTool(BaseTool):
    name: str = "Analyze User Preferences"
    description: str = "Analyze user preferences based on past events"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, user_data: dict) -> str:
        return self.agent._analyze_user_preferences(user_data)

class SimilarEventsTool(BaseTool):
    name: str = "Find Similar Events"
    description: str = "Find events that match user preferences"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, preferences: str, available_events: List[Dict]) -> List[Dict]:
        # Convert Event instances to dictionaries
        events_data = [
            {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'start_date': event.start_date.isoformat() if event.start_date else None,
                'end_date': event.end_date.isoformat() if event.end_date else None,
                'location': event.location,
                'capacity': event.capacity,
                'category': event.category.name if event.category else None
            } for event in available_events
        ]
        return self.agent._find_similar_events(preferences, events_data)

class EventScoresTool(BaseTool):
    name: str = "Calculate Event Scores"
    description: str = "Calculate recommendation scores for events"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, events: List[Dict], user_preferences: str) -> List[Dict]:
        return self.agent._calculate_event_scores(events, user_preferences)

class RegistrationPatternsTool(BaseTool):
    name: str = "Analyze Registration Patterns"
    description: str = "Analyze registration patterns for an event"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, event_data: dict) -> str:
        return self.agent._analyze_registration_patterns(event_data)

class FeedbackAnalysisTool(BaseTool):
    name: str = "Analyze Feedback Data"
    description: str = "Analyze feedback data for insights"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, feedback_data: List[Dict]) -> Dict:
        return self.agent._analyze_feedback_data(feedback_data)

class PerformanceInsightsTool(BaseTool):
    name: str = "Generate Performance Insights"
    description: str = "Generate insights from analysis data"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, analysis_data: Dict) -> List[str]:
        return self.agent._generate_performance_insights(analysis_data)

class HistoricalAnalysisTool(BaseTool):
    name: str = "Analyze Historical Data"
    description: str = "Analyze historical event data for patterns"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, event_history: List[Dict]) -> Dict:
        return self.agent._analyze_historical_data(event_history)

class OptimalParametersTool(BaseTool):
    name: str = "Predict Optimal Parameters"
    description: str = "Predict optimal event parameters"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, historical_analysis: Dict) -> Dict:
        return self.agent._predict_optimal_parameters(historical_analysis)

class MarketingStrategiesTool(BaseTool):
    name: str = "Generate Marketing Strategies"
    description: str = "Generate marketing strategies"
    agent: Any = Field(description="The agent instance that owns this tool")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_instance):
        super().__init__(agent=agent_instance)

    def _run(self, event_data: Dict) -> List[str]:
        return self.agent._generate_marketing_strategies(event_data)

class EventAnalysisAgent:
    def __init__(self):
        # Initialize Ollama with tinyllama
        self.llm = Ollama(
            base_url="http://ollama:11434",
            model="tinyllama",
            temperature=0.7
        )
        
        # Initialize recommendation prompt
        self.recommendation_prompt = PromptTemplate(
            input_variables=["user_context"],
            template="""
            As an AI event recommendation system, analyze the following user context and provide personalized event recommendations.
            
            User Context:
            {user_context}
            
            Based on this information, provide recommendations in the following JSON format:
            {
                "recommended_categories": ["category1", "category2"],
                "interests": ["interest1", "interest2"],
                "explanation": "Brief explanation of recommendations"
            }
            
            Only respond with the JSON object, no other text.
            """
        )
        
        # Create recommendation chain
        self.recommendation_chain = LLMChain(
            llm=self.llm,
            prompt=self.recommendation_prompt
        )
        
        # Initialize tools
        self.user_preferences_tool = UserPreferencesTool(self)
        self.similar_events_tool = SimilarEventsTool(self)
        self.event_scores_tool = EventScoresTool(self)
        self.registration_patterns_tool = RegistrationPatternsTool(self)
        self.feedback_analysis_tool = FeedbackAnalysisTool(self)
        self.performance_insights_tool = PerformanceInsightsTool(self)
        self.historical_analysis_tool = HistoricalAnalysisTool(self)
        self.optimal_parameters_tool = OptimalParametersTool(self)
        self.marketing_strategies_tool = MarketingStrategiesTool(self)
        
        self.recommendation_agent = Agent(
            role='Event Recommendation Specialist',
            goal='Provide personalized event recommendations based on user preferences and behavior',
            backstory='AI specialist in analyzing user preferences and event patterns to make accurate recommendations',
            verbose=True,
            llm=self.llm,
            tools=[
                self.user_preferences_tool,
                self.similar_events_tool,
                self.event_scores_tool
            ]
        )
        
        self.analysis_agent = Agent(
            role='Event Analytics Expert',
            goal='Analyze event performance and attendee behavior patterns',
            backstory='Expert in data analysis and pattern recognition for event metrics',
            verbose=True,
            llm=self.llm,
            tools=[
                self.registration_patterns_tool,
                self.feedback_analysis_tool,
                self.performance_insights_tool
            ]
        )
        
        self.optimization_agent = Agent(
            role='Event Optimization Specialist',
            goal='Optimize event parameters for maximum engagement and success',
            backstory='Specialist in improving event outcomes through data-driven insights',
            verbose=True,
            llm=self.llm,
            tools=[
                self.historical_analysis_tool,
                self.optimal_parameters_tool,
                self.marketing_strategies_tool
            ]
        )

    def get_recommendations(self, user_context):
        """Get personalized event recommendations for a user."""
        try:
            # Convert user context to string for prompt
            context_str = json.dumps(user_context, indent=2)
            
            # Get AI recommendations
            result = self.recommendation_chain.run(user_context=context_str)
            
            # Parse JSON response
            recommendations = json.loads(result)
            return recommendations
            
        except Exception as e:
            # Return default recommendations on error
            return {
                "recommended_categories": [],
                "interests": [],
                "explanation": "Unable to generate personalized recommendations"
            }

    def analyze_event_performance(self, event_id: int) -> Dict:
        """Analyze performance metrics for an event."""
        event = Event.objects.get(id=event_id)
        registrations = event.registrations.all()
        feedback = event.feedback.all()
        
        # Convert event data to dictionary
        event_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_date': event.start_date.isoformat() if event.start_date else None,
            'end_date': event.end_date.isoformat() if event.end_date else None,
            'location': event.location,
            'capacity': event.capacity,
            'categories': [cat.name for cat in event.categories.all()],
            'registrations': [
                {
                    'id': reg.id,
                    'user': reg.user.username,
                    'status': reg.status,
                    'created_at': reg.created_at.isoformat() if reg.created_at else None,
                    'attended': reg.attended
                } for reg in registrations
            ],
            'feedback': [
                {
                    'id': f.id,
                    'user': f.user.username,
                    'rating': f.rating,
                    'comment': f.comment,
                    'created_at': f.created_at.isoformat() if f.created_at else None
                } for f in feedback
            ]
        }
        
        task = Task(
            description=f"""
            Analyze the following event data and provide insights:
            Event: {event_data['title']}
            Categories: {', '.join(event_data['categories'])}
            Registrations: {len(event_data['registrations'])}
            Feedback Count: {len(event_data['feedback'])}
            Average Rating: {sum(f['rating'] for f in event_data['feedback']) / len(event_data['feedback']) if event_data['feedback'] else 0}
            
            Analyze:
            1. Registration patterns and attendance rates
            2. Feedback sentiment and common themes
            3. Event timing and capacity utilization
            4. Areas for improvement
            """,
            expected_output="""A dictionary containing analysis results:
            {
                'registration_analysis': {
                    'patterns': List[str],
                    'attendance_rate': float,
                    'peak_times': List[str]
                },
                'feedback_analysis': {
                    'sentiment': str,
                    'common_themes': List[str],
                    'average_rating': float
                },
                'capacity_analysis': {
                    'utilization_rate': float,
                    'recommendations': List[str]
                },
                'improvement_areas': List[str]
            }""",
            agent=self.analysis_agent
        )
        
        crew = Crew(
            agents=[self.analysis_agent],
            tasks=[task]
        )
        
        result = crew.kickoff()
        return self._process_analysis(result, event_data)

    def optimize_event_parameters(self, event_id: int) -> Dict:
        """Generate optimization suggestions for an event."""
        event = Event.objects.get(id=event_id)
        
        # Convert event to dictionary
        event_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_date': event.start_date.isoformat() if event.start_date else None,
            'end_date': event.end_date.isoformat() if event.end_date else None,
            'location': event.location,
            'capacity': event.capacity,
            'categories': [cat.name for cat in event.categories.all()]
        }
        
        task = Task(
            description=f"""
            Analyze and optimize the following event parameters:
            Event: {event_data['title']}
            Categories: {', '.join(event_data['categories'])}
            Current Capacity: {event_data['capacity']}
            Location: {event_data['location']}
            Timing: {event_data['start_date']} to {event_data['end_date']}
            
            Provide recommendations for:
            1. Optimal timing and duration
            2. Capacity planning
            3. Marketing strategies
            4. Engagement improvements
            """,
            expected_output="""A dictionary containing optimization recommendations:
            {
                'timing': {
                    'recommended_start': str,
                    'recommended_duration': str,
                    'reasoning': str
                },
                'capacity': {
                    'recommended_capacity': int,
                    'reasoning': str
                },
                'marketing': {
                    'strategies': List[str],
                    'target_audience': List[str]
                },
                'engagement': {
                    'suggestions': List[str],
                    'expected_impact': List[str]
                }
            }""",
            agent=self.optimization_agent
        )
        
        crew = Crew(
            agents=[self.optimization_agent],
            tasks=[task]
        )
        
        result = crew.kickoff()
        return self._process_optimization(result, event_data)
    
    def _process_recommendations(self, crew_result: str) -> List[Dict]:
        """Process the crew's recommendations into actionable insights."""
        # Get upcoming events that match the recommendations
        upcoming_events = Event.objects.filter(
            start_date__gt=timezone.now(),
            is_active=True
        ).order_by('start_date')
        
        # Filter and score events based on crew's recommendations
        recommended_events = []
        for event in upcoming_events:
            score = self._calculate_recommendation_score(event, crew_result)
            if score > 0.5:  # Threshold for recommendations
                recommended_events.append({
                    'event': event,
                    'score': score,
                    'reason': self._get_recommendation_reason(event, crew_result)
                })
        
        return sorted(recommended_events, key=lambda x: x['score'], reverse=True)

    def _process_analysis(self, result: str, event: Event, registrations: List[EventRegistration], feedback: List[EventFeedback]) -> Dict:
        """Process the analysis results into a structured format."""
        # Calculate basic metrics
        total_registrations = registrations.count()
        confirmed_registrations = registrations.filter(status='confirmed').count()
        attended = registrations.filter(attended=True).count()
        
        # Calculate rates
        registration_rate = (confirmed_registrations / event.capacity * 100) if event.capacity > 0 else 0
        attendance_rate = (attended / confirmed_registrations * 100) if confirmed_registrations > 0 else 0
        
        # Process feedback
        avg_rating = feedback.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
        
        return {
            'registration_rate': registration_rate,
            'attendance_rate': attendance_rate,
            'average_rating': avg_rating,
            'peak_registration_time': self._get_peak_registration_time(registrations),
            'feedback_sentiment': self._analyze_feedback_sentiment(feedback),
            'feedback_themes': self._extract_feedback_themes(feedback),
            'recommendations': self._generate_analysis_recommendations(result)
        }

    def _process_optimization(self, result: str, event: Event) -> Dict:
        """Process the optimization results into actionable recommendations."""
        return {
            'recommended_time': self._get_recommended_time(event, result),
            'time_reasoning': self._extract_time_reasoning(result),
            'recommended_duration': self._get_recommended_duration(event, result),
            'duration_reasoning': self._extract_duration_reasoning(result),
            'recommended_capacity': self._get_recommended_capacity(event, result),
            'capacity_reasoning': self._extract_capacity_reasoning(result),
            'expected_attendance': self._calculate_expected_attendance(event),
            'marketing_suggestions': self._extract_marketing_suggestions(result),
            'additional_recommendations': self._extract_additional_recommendations(result)
        }
    
    # Helper methods for recommendation scoring
    def _calculate_recommendation_score(self, event: Event, crew_result: str) -> float:
        """Calculate a recommendation score for an event."""
        # Implement scoring logic based on crew's analysis
        return 0.75  # Placeholder score
    
    def _get_recommendation_reason(self, event: Event, crew_result: str) -> str:
        """Generate a human-readable reason for the recommendation."""
        return "Based on your interests and past event attendance"  # Placeholder reason
    
    # Helper methods for analysis processing
    def _get_peak_registration_time(self, registrations: List[EventRegistration]) -> str:
        return "2 weeks before event"  # Placeholder
    
    def _analyze_feedback_sentiment(self, feedback: List[EventFeedback]) -> str:
        return "Mostly Positive"  # Placeholder
    
    def _extract_feedback_themes(self, feedback: List[EventFeedback]) -> List[str]:
        return ["Good organization", "Engaging content"]  # Placeholder
    
    def _generate_analysis_recommendations(self, result: str) -> List[str]:
        return ["Increase marketing efforts", "Consider larger venue"]  # Placeholder
    
    # Helper methods for optimization processing
    def _get_recommended_time(self, event: Event, result: str) -> str:
        return "Weekday evenings"  # Placeholder
    
    def _extract_time_reasoning(self, result: str) -> str:
        return "Based on attendance patterns"  # Placeholder
    
    def _get_recommended_duration(self, event: Event, result: str) -> str:
        return "2-3 hours"  # Placeholder
    
    def _extract_duration_reasoning(self, result: str) -> str:
        return "Optimal for engagement"  # Placeholder
    
    def _get_recommended_capacity(self, event: Event, result: str) -> int:
        return 100  # Placeholder
    
    def _extract_capacity_reasoning(self, result: str) -> str:
        return "Based on historical demand"  # Placeholder
    
    def _calculate_expected_attendance(self, event: Event) -> int:
        return 80  # Placeholder
    
    def _extract_marketing_suggestions(self, result: str) -> List[str]:
        return ["Use social media", "Email campaigns"]  # Placeholder
    
    def _extract_additional_recommendations(self, result: str) -> List[str]:
        return ["Add networking session", "Include refreshments"]  # Placeholder

    def _analyze_user_preferences(self, user_data: dict) -> str:
        """Analyze user preferences based on past events."""
        return f"""
        Based on the user's history:
        - Preferred Categories: {', '.join(user_data['categories'])}
        - Typical Event Times: {user_data['preferred_times']}
        - Location Preferences: {user_data['locations']}
        """

    def _find_similar_events(self, preferences: str, available_events: List[Dict]) -> List[Dict]:
        """Find events that match user preferences."""
        # Implementation using the LLM to match preferences with events
        matches = []
        for event in available_events:
            # Add your matching logic here
            pass
        return matches

    def _calculate_event_scores(self, events: List[Dict], user_preferences: str) -> List[Dict]:
        """Calculate recommendation scores for events."""
        # Implementation using the LLM to score events
        scored_events = []
        for event in events:
            # Add your scoring logic here
            pass
        return scored_events

    def _analyze_registration_patterns(self, event_data: dict) -> str:
        """Analyze registration patterns for an event."""
        return f"""
        Registration Analysis:
        - Peak Times: {event_data['peak_times']}
        - Registration Rate: {event_data['registration_rate']}%
        - Attendance Rate: {event_data['attendance_rate']}%
        """

    def _analyze_feedback_data(self, feedback_data: List[Dict]) -> Dict:
        """Analyze feedback data for insights."""
        # Implementation using the LLM to analyze feedback
        return {
            'sentiment': 'positive',
            'themes': ['Good organization', 'Engaging content'],
            'suggestions': ['Add more networking time']
        }

    def _generate_performance_insights(self, analysis_data: Dict) -> List[str]:
        """Generate insights from analysis data."""
        # Implementation using the LLM to generate insights
        return [
            "High engagement during morning sessions",
            "Networking breaks are highly valued",
            "Consider expanding capacity"
        ]

    def _analyze_historical_data(self, event_history: List[Dict]) -> Dict:
        """Analyze historical event data for patterns."""
        # Implementation using the LLM to analyze historical data
        return {
            'optimal_times': ['Weekday evenings', 'Saturday mornings'],
            'ideal_duration': '2-3 hours',
            'successful_formats': ['Workshop', 'Panel discussion']
        }

    def _predict_optimal_parameters(self, historical_analysis: Dict) -> Dict:
        """Predict optimal event parameters."""
        # Implementation using the LLM to predict parameters
        return {
            'recommended_time': 'Thursday 6 PM',
            'recommended_duration': '2.5 hours',
            'recommended_capacity': 100
        }

    def _generate_marketing_strategies(self, event_data: Dict) -> List[str]:
        """Generate marketing strategies."""
        # Implementation using the LLM to generate strategies
        return [
            "Target similar interest groups",
            "Early bird discounts",
            "Social media campaign focus"
        ] 