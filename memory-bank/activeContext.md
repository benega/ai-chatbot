# Active Context: WhatsApp Chatbot Assistant

## Current Work Focus
The project is currently focused on:

1.  **WhatsApp Integration**: Implementing basic WhatsApp message receiving and sending functionality.
2.  **Project Setup**: Establishing the basic project structure and development environment.

## Recent Changes
1.  **WhatsApp Integration**: The original WhatsApp integration code was replaced with code from another project. This involved modifying `app/whatsapp/whatsapp.py` and `app/whatsapp/whatsapp_utils.py`. The AI agent calling functionality was removed for initial testing.
2.  **Main File Replacement**: `main.py` was removed and replaced with `run.py`.

## Next Steps

### Immediate Tasks
1.  **Further develop WhatsApp message handling**: Implement more robust message processing and error handling.
2.  **Build class schedule parser**: Define CSV format for schedule data, implement parser with pandas, create availability checking logic, and add caching mechanism for performance.
3.  **Integrate AI for conversation handling**: Use Langchain and OpenAI (GPT-4 or GPT-3.5-turbo) for natural language understanding, implement Langraph for managing multiple agents (Main Conversation Agent, Schedule Agent, Booking Agent, FAQ Agent, System Coordinator), and ensure the AI can access/manage the Google Calendar as a tool.

### Planned for Near Future
1.  **Google Calendar integration**: Set up authentication, implement event creation, add invitation sending, and create update/cancel functionality.
2.  **Conversation state management**: Design state machine for conversation flow, implement persistence for active conversations, create timeout and recovery mechanisms, and add context tracking between messages.
3.  **Testing infrastructure**: Set up pytest framework, create mock objects for external dependencies, implement unit tests for core components, and add integration tests for key flows.

## Active Decisions and Considerations

### Architecture Decisions
- **Feature-based organization**: We've decided to organize the codebase by feature rather than technical layer to improve maintainability and cohesion.
- **Clean separation of concerns**: Each component will have clear responsibilities and boundaries to ensure modularity and testability.
- **Dependency injection**: Components will receive their dependencies through constructor injection to improve testability and flexibility.

### Implementation Considerations
- **CSV for schedule data**: Using CSV files for schedule data as they are simple to implement and easy for staff to update.
- **Stateful conversation management**: Maintaining conversation state between messages to enable multi-step booking process.
- **Error handling strategy**: Implementing centralized error handling with graceful degradation to ensure consistent user experience.

### Open Questions
- **Persistence mechanism**: Need to determine the best approach for persisting conversation state (in-memory, file-based, or database).
- **Deployment strategy**: Need to decide on the initial deployment environment and process.
- **Monitoring approach**: Need to establish how the system will be monitored in production.

## Important Patterns and Preferences

### Code Style
- **PEP 8**: Following Python's PEP 8 style guide for code formatting
- **Type hints**: Using Python type hints for improved code clarity and IDE support
- **Docstrings**: Comprehensive docstrings for all public functions and classes
- **Meaningful naming**: Clear, descriptive names for variables, functions, and classes

### Design Patterns
- **Adapter Pattern**: For external API integrations (WhatsApp, Google Calendar)
- **Repository Pattern**: For data access (CSV schedule data)
- **Strategy Pattern**: For intent recognition approaches
- **State Pattern**: For conversation state management
- **Chain of Responsibility**: For message processing pipeline

### Testing Approach
- **Test-driven development**: Writing tests before implementation for core components
- **Mock external dependencies**: Using pytest-mock for external API interactions
- **High coverage targets**: Aiming for 90%+ coverage on core business logic
- **Integration testing**: Testing component interactions in addition to unit tests

## Learnings and Project Insights

### Initial Insights
- The WhatsApp Cloud API has specific requirements for webhook verification that need to be handled correctly
- Google Calendar API requires careful scope management for proper authorization
- CSV parsing with pandas offers significant performance advantages over manual parsing

### Challenges Identified
- Maintaining conversation context across multiple messages will require careful state management
- Intent recognition accuracy will be critical for good user experience
- Handling edge cases in schedule availability checking will be complex

### Opportunities
- The modular architecture will allow for easy extension to additional features in the future
- The conversation framework could be reused for other chatbot applications
- Data collected could provide valuable insights into class popularity and booking patterns

## Revision History
- v1.0 (Initial version): Project initialization

## AI Integration Implementation Steps

1. **Set up the AI environment:**
   - Create the `app/ai/` directory and its subdirectories (agents, tools, memory, prompts, models, conversation).
   - **User Feedback**: After this step, the user should verify that the directories have been created correctly.

2. **Install dependencies:**
   - Add the necessary Langchain, OpenAI, and Langraph dependencies to `requirements.txt`.
   - Install the dependencies using `pip install -r requirements.txt`.
   - **User Feedback**: After this step, the user should verify that the dependencies have been installed correctly.

3. **Design the AI components:**
   - Define the structure and functionality of the agents (Main Conversation Agent, Schedule Agent, Booking Agent, FAQ Agent).
   - Implement the Langchain tools (Google Calendar Tool, Schedule Checker Tool, FAQ Retrieval Tool).
   - Configure the Langchain memory components.
   - Create the PromptTemplates for different intents and agent interactions.
   - **User Feedback**: After this step, the user should review the design and provide feedback.

4. **Implement the AI integration:**
   - Integrate the AI components with the existing WhatsApp API, Google Calendar API, and CSV schedule data.
   - Route messages to the AI Conversation Handler.
   - Use the Google Calendar Tool to create calendar events.
   - Use the Schedule Checker Tool to query the CSV schedule data.
   - **User Feedback**: After this step, the user should test the integration and provide feedback.

5. **Test the AI integration:**
   - Create unit tests for the AI components.
   - Create integration tests for the AI integration with external APIs.
   - **User Feedback**: After this step, the user should review the test results and provide feedback.

6. **Document the AI integration:**
   - Update the documentation to reflect the new AI integration.
   - **User Feedback**: After this step, the user should review the documentation and provide feedback.

**Note:** After each step, I will wait for your confirmation before proceeding to the next step. This will allow you to provide feedback and ensure that the implementation is aligned with your expectations.

## AI Integration Next Steps

1. **Set up the AI environment:**
   - Create the `app/ai/` directory and its subdirectories (agents, tools, memory, prompts, models, conversation).

2. **Install dependencies:**
   - Add the necessary Langchain, OpenAI, and Langraph dependencies to `requirements.txt`.
   - Install the dependencies using `pip install -r requirements.txt`.

3. **Design the AI components:**
   - Define the structure and functionality of the agents (Main Conversation Agent, Schedule Agent, Booking Agent, FAQ Agent).
   - Implement the Langchain tools (Google Calendar Tool, Schedule Checker Tool, FAQ Retrieval Tool).
   - Configure the Langchain memory components.
   - Create the PromptTemplates for different intents and agent interactions.

4. **Implement the AI integration:**
   - Integrate the AI components with the existing WhatsApp API, Google Calendar API, and CSV schedule data.
   - Route messages to the AI Conversation Handler.
   - Use the Google Calendar Tool to create calendar events.
   - Use the Schedule Checker Tool to query the CSV schedule data.

5. **Test the AI integration:**
   - Create unit tests for the AI components.
   - Create integration tests for the AI integration with external APIs.

6. **Document the AI integration:**
   - Update the documentation to reflect the new AI integration.
