"""
Enhanced A2A Agent Executor demonstrating all protocol features.

This executor demonstrates:
1. All task states (submitted, working, input-required, completed, canceled, failed)
2. All content types (TextPart, FilePart, DataPart)
3. Different response patterns
4. Error handling
5. Long-running tasks with progress updates
6. Input requirements
7. Artifact generation
8. Push notifications
"""

from typing import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    DataPart,
    FilePart,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
)
from a2a.utils import new_agent_text_message, new_task, new_text_artifact, new_data_artifact

from enhanced_agent import EnhancedAgent


class EnhancedAgentExecutor(AgentExecutor):
    """Enhanced Agent Executor demonstrating all A2A protocol features."""

    def __init__(self):
        self.agent = EnhancedAgent(
            mode='stream',
            token_stream_callback=print,
        )

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute the enhanced agent with full A2A protocol support."""
        query = context.get_user_input()
        task = context.current_task

        if not context.message:
            raise Exception('No message provided')

        if not task:
            print(f"🔧 Creating new task for message with task_id: {context.message.task_id}")
            # Use the task ID from the message if it exists, otherwise create a new task
            if context.message.task_id:
                # Create task with the existing task ID from the message
                task = new_task(context.message)
                # Ensure the task ID matches the message
                task.id = context.message.task_id
                print(f"🔧 Created task with ID: {task.id}")
            else:
                task = new_task(context.message)
                print(f"🔧 Created task with new ID: {task.id}")
            
            # Enqueue the task creation event
            await event_queue.enqueue_event(task)
            print(f"🔧 Enqueued task creation event for task: {task.id}")
            
            # Also enqueue a status update to ensure the task is properly initialized
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(state=TaskState.submitted),
                    final=False,
                    context_id=task.context_id,
                    task_id=task.id,
                )
            )
            print(f"🔧 Enqueued task status update for task: {task.id}")

        # Check for different content types in the message
        has_file_content = False
        has_structured_data = False
        file_content = ""
        structured_data = None

        if context.message.parts:
            for part in context.message.parts:
                if hasattr(part.root, 'file') and part.root.file:
                    has_file_content = True
                    if hasattr(part.root.file, 'bytes') and part.root.file.bytes:
                        import base64
                        file_content = base64.b64decode(part.root.file.bytes).decode('utf-8')
                elif hasattr(part.root, 'data') and part.root.data:
                    has_structured_data = True
                    structured_data = part.root.data

        # Process based on content type
        if has_file_content:
            await self._process_file_content(context, event_queue, task, file_content, query)
        elif has_structured_data:
            await self._process_structured_data(context, event_queue, task, structured_data, query)
        else:
            await self._process_text_content(context, event_queue, task, query)

    async def _process_text_content(self, context: RequestContext, event_queue: EventQueue, task, query: str):
        """Process text content with full A2A protocol support."""
        async for event in self.agent.stream(query):
            if event['is_task_complete']:
                # Create final artifact
                await event_queue.enqueue_event(
                    TaskArtifactUpdateEvent(
                        append=False,
                        context_id=task.context_id,
                        task_id=task.id,
                        last_chunk=True,
                        artifact=new_text_artifact(
                            name='final_result',
                            description='Final result of the request.',
                            text=event['content'],
                        ),
                    )
                )
                # Set final status
                task_state = TaskState(event['task_state'])
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(state=task_state),
                        final=True,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )
            elif event['require_user_input']:
                # Handle input required state
                task_state = TaskState(event['task_state'])
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=task_state,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id,
                            ),
                        ),
                        final=True,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )
            else:
                # Handle working state with progress updates
                task_state = TaskState(event['task_state'])
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        append=True,
                        status=TaskStatus(
                            state=task_state,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id,
                            ),
                        ),
                        final=False,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )

    async def _process_file_content(self, context: RequestContext, event_queue: EventQueue, task, file_content: str, query: str):
        """Process file content with file-specific handling."""
        # First, acknowledge file receipt
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                append=True,
                status=TaskStatus(
                    state=TaskState.working,
                    message=new_agent_text_message(
                        f"Received file content ({len(file_content)} characters). Processing...",
                        task.context_id,
                        task.id,
                    ),
                ),
                final=False,
                context_id=task.context_id,
                task_id=task.id,
            )
        )

        # Create file artifact
        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                append=False,
                context_id=task.context_id,
                task_id=task.id,
                last_chunk=False,
                artifact=new_text_artifact(
                    name='input_file',
                    description='Input file content for processing.',
                    text=file_content,
                ),
            )
        )

        # Process the file content
        async for event in self.agent.stream(f"file: {query}"):
            if event['is_task_complete']:
                # Create final artifact with file analysis
                await event_queue.enqueue_event(
                    TaskArtifactUpdateEvent(
                        append=False,
                        context_id=task.context_id,
                        task_id=task.id,
                        last_chunk=True,
                        artifact=new_text_artifact(
                            name='file_analysis_result',
                            description='Analysis result of the input file.',
                            text=event['content'],
                        ),
                    )
                )
                # Set final status
                task_state = TaskState(event['task_state'])
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(state=task_state),
                        final=True,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )
            else:
                # Handle progress updates
                task_state = TaskState(event['task_state'])
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        append=True,
                        status=TaskStatus(
                            state=task_state,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id,
                            ),
                        ),
                        final=False,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )

    async def _process_structured_data(self, context: RequestContext, event_queue: EventQueue, task, structured_data, query: str):
        """Process structured data with form-specific handling."""
        # First, acknowledge structured data receipt
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                append=True,
                status=TaskStatus(
                    state=TaskState.working,
                    message=new_agent_text_message(
                        f"Received structured data. Processing form...",
                        task.context_id,
                        task.id,
                    ),
                ),
                final=False,
                context_id=task.context_id,
                task_id=task.id,
            )
        )

        # Create structured data artifact
        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                append=False,
                context_id=task.context_id,
                task_id=task.id,
                last_chunk=False,
                artifact=new_data_artifact(
                    name='input_form_data',
                    description='Input form data for processing.',
                    data=structured_data,
                ),
            )
        )

        # Process the structured data
        async for event in self.agent.stream(f"form: {query}"):
            if event['is_task_complete']:
                # Create final artifact with form processing result
                await event_queue.enqueue_event(
                    TaskArtifactUpdateEvent(
                        append=False,
                        context_id=task.context_id,
                        task_id=task.id,
                        last_chunk=True,
                        artifact=new_text_artifact(
                            name='form_processing_result',
                            description='Result of form data processing.',
                            text=event['content'],
                        ),
                    )
                )
                # Set final status
                task_state = TaskState(event['task_state'])
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(state=task_state),
                        final=True,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )
            else:
                # Handle progress updates
                task_state = TaskState(event['task_state'])
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        append=True,
                        status=TaskStatus(
                            state=task_state,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id,
                            ),
                        ),
                        final=False,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )

    @override
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Handle task cancellation."""
        task = context.current_task
        if task:
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(state=TaskState.canceled),
                    final=True,
                    context_id=task.context_id,
                    task_id=task.id,
                )
            )
        else:
            raise Exception('No task to cancel') 
