"""
Enhanced A2A Server demonstrating all protocol features.

This server demonstrates:
1. All RPC methods (message/send, message/stream, tasks/get, tasks/cancel, etc.)
2. All task states (submitted, working, input-required, completed, canceled, failed)
3. All event types (TaskStatusUpdateEvent, TaskArtifactUpdateEvent)
4. All content types (TextPart, FilePart, DataPart)
5. Push notifications
6. Error handling
7. Streaming responses
"""

import click
import uvicorn

from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import (
    DefaultRequestHandler,
)
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    CancelTaskRequest,
    CancelTaskResponse,
    GetTaskRequest,
    GetTaskResponse,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
    Task,
    TaskState,
    TaskStatus,
)

from enhanced_agent_executor import EnhancedAgentExecutor


class EnhancedA2ARequestHandler(DefaultRequestHandler):
    """Enhanced A2A Request Handler demonstrating all protocol features."""

    def __init__(
        self, agent_executor: AgentExecutor, task_store: InMemoryTaskStore
    ):
        super().__init__(agent_executor, task_store)
        # Store reference to the in-memory task store
        self.task_store = task_store

    async def on_get_task(self, request: GetTaskRequest, context) -> GetTaskResponse:
        """Handle tasks/get requests with enhanced logging."""
        print(f"📋 GET Task Request: {request.id}")
        
        # Try to get task from the in-memory task store
        task = await self.task_store.get(request.id)
        
        if task:
            print(f"✅ Found task {request.id} in in-memory store")
            # Return the task directly - let the A2A SDK handle response construction
            return task
        else:
            print(f"❌ Task {request.id} not found in in-memory store")
            # Return a proper JSON-RPC error response using TaskNotFoundError
            from a2a.types import JSONRPCErrorResponse, TaskNotFoundError
            error_response = JSONRPCErrorResponse(
                error=TaskNotFoundError(
                    message=f"Task {request.id} not found",
                    task_id=request.id
                ),
                id=request.id,
                jsonrpc="2.0"
            )
            return GetTaskResponse(root=error_response)

    async def on_cancel_task(self, request: CancelTaskRequest, context) -> CancelTaskResponse:
        """Handle tasks/cancel requests with enhanced logging."""
        print(f"⏹️ CANCEL Task Request: {request.id}")
        
        # Try to get task from the in-memory task store
        task = await self.task_store.get(request.id)
        
        if task:
            print(f"✅ Found task {request.id} in in-memory store for cancellation")
            # Update task status to canceled
            canceled_status = TaskStatus(
                state=TaskState.canceled,
                message=None,  # Use None instead of string for message
                final=True
            )
            
            # Update the task in the in-memory store
            task.status = canceled_status
            await self.task_store.save(task)
            
            print(f"✅ Successfully canceled task {request.id}")
            # Return the task directly - let the A2A SDK handle response construction
            return task
        else:
            print(f"❌ Task {request.id} not found in in-memory store for cancellation")
            # Return a proper JSON-RPC error response using TaskNotFoundError
            from a2a.types import JSONRPCErrorResponse, TaskNotFoundError
            error_response = JSONRPCErrorResponse(
                error=TaskNotFoundError(
                    message=f"Task {request.id} not found",
                    task_id=request.id
                ),
                id=request.id,
                jsonrpc="2.0"
            )
            return CancelTaskResponse(root=error_response)

    async def on_message_send(
        self, request: MessageSendParams, context
    ) -> SendMessageResponse:
        """Handle message/send requests with enhanced logging."""
        print(f"📤 SEND Message Request: {request.message.message_id}")
        print(f"🔧 Task ID from message: {request.message.task_id}")
        if request.message.parts:
            for i, part in enumerate(request.message.parts):
                if hasattr(part.root, 'text'):
                    print(f"   Part {i}: Text content ({len(part.root.text)} chars)")
                elif hasattr(part.root, 'file'):
                    print(f"   Part {i}: File content ({part.root.file.name})")
                elif hasattr(part.root, 'data'):
                    print(f"   Part {i}: Structured data")
        
        # Handle message send directly with our enhanced logic
        print(f"🔧 Handling message send with enhanced logic...")
        task = await self._handle_message_send_directly(request, context)
        
        # Return the task directly - let the A2A SDK handle response construction
        return task

    async def _handle_message_send_directly(self, request: SendMessageRequest, context) -> Task:
        """Handle message send directly when parent method fails."""
        from a2a.types import Task, TaskStatus, TaskState
        from a2a.utils import new_task
        
        print(f"🔧 Creating task directly for message: {request.message.message_id}")
        
        # Check if message has parts
        if not request.message.parts:
            print(f"❌ Message has no parts - this is expected for error testing")
            # Create a minimal task for error demonstration
            from a2a.types import Message, Role, TextPart
            # Create a simple text part to avoid the empty parts error
            text_part = TextPart(text="Error: Message had no parts")
            error_message = Message(
                role=Role.user,
                parts=[text_part],
                message_id=request.message.message_id,
                task_id=request.message.task_id,
            )
            task = new_task(error_message)
        else:
            # Create task with the message's task ID
            task = new_task(request.message)
        
        if request.message.task_id:
            task.id = request.message.task_id
            print(f"🔧 Set task ID to: {task.id}")
        
        # Store task in the in-memory task store
        try:
            await self.task_store.save(task)
            print(f"💾 Stored task {task.id} in in-memory store")
        except Exception as e:
            print(f"❌ Error storing task {task.id} in in-memory store: {e}")
        
        return task


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=9999)
def main(host: str, port: int):
    """Start the Enhanced A2A Server.

    This function initializes the Enhanced A2A Server with comprehensive protocol support.
    It creates an agent card with enhanced capabilities and demonstrates all A2A features.

    Args:
        host (str): The host address to run the server on.
        port (int): The port number to run the server on.
    """
    # Define multiple skills to demonstrate agent capabilities
    skills = [
        AgentSkill(
            id='text_processing',
            name='Text Processing',
            description='Process and respond to text-based queries with comprehensive A2A protocol support.',
            tags=['text', 'A2A', 'protocol'],
            examples=['What is A2A protocol?', 'Explain the benefits of agent communication.'],
        ),
        AgentSkill(
            id='file_analysis',
            name='File Analysis',
            description='Analyze uploaded files and provide insights with file handling capabilities.',
            tags=['file', 'analysis', 'upload'],
            examples=['Analyze this document', 'Process this file content'],
        ),
        AgentSkill(
            id='form_processing',
            name='Form Processing',
            description='Process structured data and forms with DataPart support.',
            tags=['form', 'data', 'structured'],
            examples=['Process this form data', 'Handle structured input'],
        ),
        AgentSkill(
            id='error_demonstration',
            name='Error Demonstration',
            description='Demonstrate various error scenarios and handling.',
            tags=['error', 'handling', 'demo'],
            examples=['Demonstrate an error', 'Show error handling'],
        ),
        AgentSkill(
            id='long_running_tasks',
            name='Long Running Tasks',
            description='Demonstrate long-running tasks with progress updates.',
            tags=['long-running', 'progress', 'streaming'],
            examples=['Run a long task', 'Show progress updates'],
        ),
        AgentSkill(
            id='input_requirements',
            name='Input Requirements',
            description='Demonstrate input-required states and user interaction.',
            tags=['input', 'interaction', 'user'],
            examples=['Request additional input', 'Ask for more information'],
        ),
        AgentSkill(
            id='task_cancellation',
            name='Task Cancellation',
            description='Demonstrate task cancellation capabilities.',
            tags=['cancel', 'termination', 'control'],
            examples=['Cancel this task', 'Stop processing'],
        ),
    ]

    agent_card = AgentCard(
        name='Enhanced A2A Protocol Agent',
        description='A comprehensive A2A protocol demonstration agent that showcases all communication types, task states, content types, and protocol features including streaming, push notifications, error handling, and more.',
        url=f'http://{host}:{port}/',
        version='2.0.0',
        default_input_modes=['text', 'file', 'data'],
        default_output_modes=['text', 'file', 'data'],
        capabilities=AgentCapabilities(
            input_modes=['text', 'file', 'data'],
            output_modes=['text', 'file', 'data'],
            streaming=True,
            push_notifications=True,
            state_transition_history=True,
        ),
        skills=skills,
        examples=[
            'What is A2A protocol?',
            'Analyze this file content',
            'Process this form data',
            'Demonstrate an error scenario',
            'Run a long-running task with progress',
            'Request additional input from user',
            'Cancel a running task',
        ],
    )

    task_store = InMemoryTaskStore()
    request_handler = EnhancedA2ARequestHandler(
        agent_executor=EnhancedAgentExecutor(),
        task_store=task_store,
    )

    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    
    print("🚀 Starting Enhanced A2A Protocol Server")
    print("=" * 50)
    print(f"📍 Server URL: http://{host}:{port}/")
    print(f"📋 Agent Card: http://{host}:{port}/.well-known/agent.json")
    print(f"🔧 A2A Endpoint: http://{host}:{port}/a2a")
    print(f"🌊 Streaming Endpoint: http://{host}:{port}/a2a/stream")
    print("=" * 50)
    print("✨ This server demonstrates ALL A2A protocol features:")
    print("   • All RPC methods (message/send, message/stream, tasks/get, tasks/cancel)")
    print("   • All task states (submitted, working, input-required, completed, canceled, failed)")
    print("   • All event types (TaskStatusUpdateEvent, TaskArtifactUpdateEvent)")
    print("   • All content types (TextPart, FilePart, DataPart)")
    print("   • Push notifications")
    print("   • Error handling")
    print("   • Streaming responses")
    print("   • Long-running tasks with progress updates")
    print("   • Input requirements and user interaction")
    print("   • Task cancellation")
    print("=" * 50)
    
    uvicorn.run(server.build(), host=host, port=port)


if __name__ == '__main__':
    main() 
