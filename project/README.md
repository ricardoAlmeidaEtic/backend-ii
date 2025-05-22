# Event Management System with AI Integration

This project is an event management system that leverages AI capabilities through Crew AI for enhanced user experience and automated processes.

## Features

- Event management and organization
- AI-powered recommendations and insights
- RESTful API endpoints
- Secure authentication and authorization
- Real-time data analysis

## Technology Stack

- Python 3.12
- Django 5.2.1
- Django REST Framework 3.16.0
- Crew AI 0.120.1
- PostgreSQL (via psycopg2-binary)
- Python-dotenv for environment management

## Project Structure

```
project/
├── api/                 # REST API implementation
├── ai_agents/           # AI agents using Crew AI
├── backend/            # Core backend services
├── frontend/           # Frontend components
└── manage.py          # Django management script
```

## Setup Instructions

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
Create a `.env` file with:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

3. Run migrations:
```bash
poetry run python manage.py migrate
```

4. Start the development server:
```bash
poetry run python manage.py runserver
```

## AI Agents

The system uses Crew AI for:
- Event recommendations
- Attendance predictions
- Content optimization
- User behavior analysis

## API Documentation

API endpoints are available at `/api/v1/` with the following main resources:
- Events
- Users
- Recommendations
- Analytics

## Security

- JWT-based authentication
- Role-based access control
- Input validation
- Secure data storage

## Error Handling

The system implements comprehensive error handling with:
- Detailed error logging
- Custom exception handling
- User-friendly error messages
- Monitoring and alerting
