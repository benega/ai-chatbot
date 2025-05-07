# Python Code Style & Patterns Guide

## 1. Code Formatting & Style

### PEP 8 Compliance
- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines
- Use 4 spaces for indentation (no tabs)
- Limit lines to 88 characters (Black default)
- Use appropriate whitespace for readability

### Naming Conventions
- `snake_case` for variables, functions, methods, modules
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants
- Prefix private attributes/methods with underscore: `_private_method()`
- Descriptive names that indicate purpose or behavior

### Imports
- Group imports in the following order:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- Sort imports alphabetically within each group
- Use absolute imports for clarity
- Use import statements (not `from x import *`)

```python
# Correct import ordering
import os
import sys
from typing import Dict, List, Optional, Union

import pandas as pd
import requests

from myapp.models import User
from myapp.utils.helpers import format_response
```

### Comments & Documentation
- Use docstrings for all public modules, functions, classes, and methods
- Follow Google-style docstrings for consistency
- Include type hints using Python's type annotation system
- Document parameters, return values, and raised exceptions
- Add comments only when necessary to explain "why", not "what"

```python
def parse_schedule(filepath: str) -> Dict[str, Dict[str, str]]:
    """Parse class schedule from CSV file.
    
    Args:
        filepath: Path to the CSV schedule file
        
    Returns:
        Dictionary with time slots as keys and day-to-class mappings as values
        
    Raises:
        FileNotFoundError: If the specified file does not exist
        ValueError: If the CSV format is invalid
    """
    # Implementation here
```

## 2. Project Structure

### Feature-Based Organization
```
src/
  ├── __init__.py
  ├── main.py              # Application entry point
  ├── whatsapp/            # WhatsApp integration
  │   ├── __init__.py
  │   ├── client.py        # WhatsApp API client
  │   ├── handlers.py      # Message handlers
  │   └── models.py        # Message data models
  ├── schedule/            # Schedule management
  │   ├── __init__.py
  │   ├── parser.py        # CSV parsing logic
  │   └── availability.py  # Availability checking
  ├── intent/              # User intent recognition
  │   ├── __init__.py
  │   ├── classifier.py    # Intent classification logic
  │   └── entities.py      # Entity extraction (dates, classes)
  ├── calendar/            # Calendar integration
  │   ├── __init__.py
  │   ├── client.py        # Google Calendar API client
  │   └── events.py        # Event creation/management
  ├── config/              # Configuration management
  │   ├── __init__.py
  │   └── settings.py      # Application settings
  ├── utils/               # Shared utilities
  │   ├── __init__.py
  │   ├── logging.py       # Logging configuration
  │   └── validators.py    # Input validation helpers
tests/                     # Test directory
  ├── conftest.py          # pytest fixtures
  ├── test_whatsapp/       # Tests for WhatsApp components
  ├── test_schedule/       # Tests for schedule components
  └── ...
data/                      # Data directory
  └── schedules/           # Schedule CSV files
```

## 3. Design Patterns & Best Practices

### Dependency Injection
- Pass dependencies as arguments rather than instantiating inside functions
- Makes testing easier by allowing mocks to be injected

```python
# Good: Dependency injection
def process_message(message: str, intent_classifier, schedule_service):
    intent = intent_classifier.classify(message)
    if intent.type == 'booking':
        return schedule_service.check_availability(intent.class_type)

# Avoid: Hard-coded dependencies
def process_message_bad(message: str):
    classifier = IntentClassifier()  # Hard to mock for testing
    intent = classifier.classify(message)
    # ...
```

### Service Layer Pattern
- Create service classes for specific functionality domains
- Services encapsulate business logic and interact with external systems

```python
class ScheduleService:
    def __init__(self, schedule_repository):
        self.repository = schedule_repository
    
    def get_available_classes(self, day: str, time_slot: Optional[str] = None) -> List[str]:
        """Get available classes for a specific day and optional time slot."""
        # Implementation
```

### Repository Pattern
- Use repositories to abstract data access
- Separate data retrieval logic from business logic

```python
class ScheduleRepository:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
    def load_schedule(self) -> Dict:
        """Load schedule data from CSV file."""
        # Implementation
        
    def get_classes_by_day(self, day: str) -> Dict[str, str]:
        """Get all classes for a specific day."""
        # Implementation
```

### Factory Pattern
- Use factories to create complex objects or when creation logic should be centralized

```python
class ResponseFactory:
    @staticmethod
    def create_availability_response(available_classes: List[str]) -> Dict:
        """Create a structured response for available classes."""
        if not available_classes:
            return {"text": "Sorry, no classes are available for that time."}
        
        class_list = ", ".join(available_classes)
        return {
            "text": f"We have these classes available: {class_list}",
            "quick_replies": [{"title": cls, "id": cls} for cls in available_classes]
        }
```

### Configuration Management
- Use environment variables for sensitive configuration
- Load configuration from files for development environments
- Centralize configuration access

```python
# config/settings.py
import os
from typing import Dict, Any
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings, loaded from environment variables."""
    WHATSAPP_API_KEY: str
    GOOGLE_CALENDAR_ID: str
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        
settings = Settings()  # Create singleton instance
```

### Error Handling
- Use custom exceptions for domain-specific errors
- Handle exceptions at appropriate levels
- Provide meaningful error messages

```python
class ScheduleError(Exception):
    """Base exception for schedule-related errors."""
    pass
    
class ScheduleParseError(ScheduleError):
    """Raised when there's an error parsing the schedule file."""
    pass

# Usage
try:
    schedule = schedule_repository.load_schedule()
except FileNotFoundError:
    logger.error("Schedule file not found")
    raise ScheduleParseError("Could not find schedule file")
except pd.errors.ParserError:
    logger.error("Invalid schedule format")
    raise ScheduleParseError("Invalid schedule format")
```

## 4. Testing Guidelines

### Test Organization
- Structure tests to mirror the application structure
- Name test files with `test_` prefix
- Group tests by feature or function

### Test Coverage
- Aim for high test coverage (>80%)
- Focus on testing business logic thoroughly
- Use pytest fixtures for common test setup

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_schedule_repository():
    repo = Mock()
    repo.load_schedule.return_value = {
        "8h-9h": {"monday": "yoga", "tuesday": "martial art"},
        "9h-10h": {"monday": "martial", "tuesday": "acrobacia"}
    }
    return repo
    
# test_schedule_service.py
def test_get_available_classes(mock_schedule_repository):
    service = ScheduleService(mock_schedule_repository)
    classes = service.get_available_classes("monday")
    assert "yoga" in classes
    assert "martial" in classes
```

### Mocking
- Use mocks for external dependencies (APIs, databases)
- Create fixtures for common mocks
- Test both success and error scenarios

```python
def test_calendar_event_creation(mocker):
    # Mock Google Calendar API
    mock_calendar_api = mocker.patch('myapp.calendar.client.GoogleCalendar')
    mock_instance = mock_calendar_api.return_value
    mock_instance.create_event.return_value = {"id": "event123"}
    
    # Test the calendar service
    calendar_service = CalendarService(calendar_client=mock_instance)
    result = calendar_service.book_class("yoga", "2023-05-10", "8h-9h", "user@example.com")
    
    # Assertions
    assert result["id"] == "event123"
    mock_instance.create_event.assert_called_once()
```

## 5. Linting & Code Quality

### Tools
- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Style guide enforcement
- **Mypy**: Static type checking
- **Bandit**: Security vulnerability scanning

### Pre-commit Hooks
Configure pre-commit hooks to automatically check code quality:

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-requests, pydantic]
-   repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
    -   id: bandit
```

## 6. Common Patterns for AI Integration

### Strategy Pattern for Intent Handlers
- Use different strategies for handling different user intents
- Register handlers in a central registry

```python
class IntentHandler:
    """Base class for intent handlers."""
    
    def can_handle(self, intent: str) -> bool:
        """Check if this handler can process the given intent."""
        raise NotImplementedError
        
    def handle(self, intent: str, entities: Dict, context: Dict) -> Dict:
        """Process the intent and return a response."""
        raise NotImplementedError

class BookingIntentHandler(IntentHandler):
    def __init__(self, schedule_service, calendar_service):
        self.schedule_service = schedule_service
        self.calendar_service = calendar_service
    
    def can_handle(self, intent: str) -> bool:
        return intent == "book_class"
        
    def handle(self, intent: str, entities: Dict, context: Dict) -> Dict:
        class_type = entities.get("class_type")
        day = entities.get("day")
        time_slot = entities.get("time_slot")
        
        available = self.schedule_service.is_available(class_type, day, time_slot)
        if available:
            # Booking logic
            return {"response_type": "confirmation", "message": "Would you like to book this class?"}
        else:
            # Unavailable logic
            return {"response_type": "unavailable", "message": "That class is not available."}

# Handler registry
class IntentHandlerRegistry:
    def __init__(self):
        self.handlers = []
        
    def register(self, handler: IntentHandler):
        self.handlers.append(handler)
        
    def get_handler(self, intent: str) -> Optional[IntentHandler]:
        for handler in self.handlers:
            if handler.can_handle(intent):
                return handler
        return None
```

### Chain of Responsibility for Message Processing
- Process messages through a series of handlers
- Each handler decides whether to process the message or pass it to the next handler

```python
class MessageProcessor:
    def __init__(self, next_processor=None):
        self.next_processor = next_processor
    
    def process(self, message: Dict) -> Optional[Dict]:
        """Process the message or pass to the next processor."""
        result = self._process_message(message)
        if result:
            return result
        elif self.next_processor:
            return self.next_processor.process(message)
        return None
    
    def _process_message(self, message: Dict) -> Optional[Dict]:
        """Internal processing logic. Should be overridden by subclasses."""
        raise NotImplementedError

class GreetingProcessor(MessageProcessor):
    def _process_message(self, message: Dict) -> Optional[Dict]:
        text = message.get("text", "").lower()
        if any(greeting in text for greeting in ["hello", "hi", "hey"]):
            return {"type": "greeting", "response": "Hello! How can I help you today?"}
        return None
```

### State Pattern for Conversation Management
- Manage conversation flow using state objects
- Each state handles messages differently based on conversation context

```python
class ConversationState:
    def handle_message(self, message: str, context: Dict) -> Tuple[str, Dict]:
        """Process message and return response with updated context."""
        raise NotImplementedError
    
    def get_next_state(self, message: str, context: Dict) -> 'ConversationState':
        """Determine the next state based on message and context."""
        raise NotImplementedError

class InitialState(ConversationState):
    def handle_message(self, message: str, context: Dict) -> Tuple[str, Dict]:
        # Initial greeting logic
        return "Welcome! How can I help you today?", context
    
    def get_next_state(self, message: str, context: Dict) -> 'ConversationState':
        intent = detect_intent(message)
        if intent == "book_class":
            return BookingState()
        elif intent == "ask_schedule":
            return ScheduleQueryState()
        return self  # Stay in the same state

class ConversationManager:
    def __init__(self, initial_state: ConversationState):
        self.state = initial_state
        self.context = {}
    
    def process_message(self, message: str) -> str:
        """Process the incoming message and return a response."""
        response, self.context = self.state.handle_message(message, self.context)
        self.state = self.state.get_next_state(message, self.context)
        return response
```

## 7. API Client Design

### Clean API Clients
- Use clean interfaces for external API interactions
- Handle authentication and errors consistently
- Allow for easy mocking in tests

```python
class WhatsAppClient:
    """Client for interacting with WhatsApp Cloud API."""
    
    def __init__(self, api_key: str, phone_number_id: str):
        self.api_key = api_key
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/v13.0/{phone_number_id}/messages"
        
    def send_message(self, recipient: str, message: str) -> Dict:
        """Send a text message to a WhatsApp user.
        
        Args:
            recipient: The recipient's phone number
            message: The message text to send
            
        Returns:
            API response as dictionary
            
        Raises:
            WhatsAppApiError: If the API request fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"WhatsApp API error: {e}")
            raise WhatsAppApiError(f"Failed to send message: {str(e)}")
```

### Retry Logic for External APIs
- Implement exponential backoff for API retries
- Handle transient failures gracefully

```python
def retry_with_backoff(retries=3, backoff_in_seconds=1):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < retries:
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, ConnectionError) as e:
                    wait_time = backoff_in_seconds * (2 ** retry_count)
                    logger.warning(f"Retrying in {wait_time} seconds: {str(e)}")
                    time.sleep(wait_time)
                    retry_count += 1
            # Last attempt
            return func(*args, **kwargs)
        return wrapper
    return decorator

class GoogleCalendarClient:
    # ...
    
    @retry_with_backoff(retries=3)
    def create_event(self, event_data: Dict) -> Dict:
        """Create a new calendar event with retry logic."""
        # Implementation
```

## 8. Additional Guidelines

### Logging Strategy
- Use different log levels appropriately (DEBUG, INFO, WARNING, ERROR)
- Include contextual information in log messages
- Configure structured logging for easier analysis

```python
import logging
import json
from datetime import datetime

class StructuredLogFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if available
        if hasattr(record, "extra"):
            log_data.update(record.extra)
            
        return json.dumps(log_data)

# Usage
logger = logging.getLogger("myapp")
logger.info("Processing message", extra={"user_id": "12345", "message_type": "text"})
```

### Environment Setup
- Use virtual environments for dependency isolation
- Define dependencies in `requirements.txt` or `pyproject.toml`
- Separate development and production dependencies

```
# requirements.txt
# Application dependencies
requests==2.28.2
pandas==2.0.0
google-auth==2.16.2
google-api-python-client==2.80.0
pydantic==1.10.7
python-dotenv==1.0.0
langchain==0.0.208
openai==0.27.4

# Development dependencies
pytest==7.3.1
pytest-mock==3.10.0
black==23.3.0
isort==5.12.0
flake8==6.0.0
mypy==1.3.0
bandit==1.7.5
pre-commit==3.3.1
```

### Continuous Integration
- Set up GitHub Actions or similar CI tool
- Run tests, linting, and type checking on each PR
- Enforce code quality standards automatically

```yaml
# .github/workflows/python-ci.yml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: Lint with flake8
      run: flake8 src tests
    - name: Check formatting with black
      run: black --check src tests
    - name: Check imports with isort
      run: isort --check-only --profile black src tests
    - name: Type check with mypy
      run: mypy src
    - name: Security check with bandit
      run: bandit -r src
    - name: Test with pytest
      run: pytest --cov=src tests/
```

This style guide provides a comprehensive framework for maintaining high-quality Python code in your WhatsApp chatbot project. Following these guidelines will help ensure your code is maintainable, testable, and follows industry best practices.