"""
Enhanced A2A Agent demonstrating all protocol features.

This agent demonstrates:
1. All task states (submitted, working, input-required, completed, canceled, failed)
2. All content types (TextPart, FilePart, DataPart)
3. Different response patterns
4. Error handling
5. Long-running tasks with progress updates
6. Input requirements
7. Artifact generation
"""

import asyncio
import json
import time
from collections.abc import AsyncGenerator, Callable, Generator
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from google import genai
from jinja2 import Template

import os

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


class EnhancedAgent:
    """Enhanced Agent demonstrating all A2A protocol features."""

    def __init__(
        self,
        mode: Literal['complete', 'stream'] = 'stream',
        token_stream_callback: Callable[[str], None] | None = None,
    ):
        self.mode = mode
        self.token_stream_callback = token_stream_callback
        self.task_counter = 0

    def call_llm(self, prompt: str) -> Generator[str, None]:
        """Call the LLM with the given prompt and return a generator of responses."""
        client = genai.Client(vertexai=False, api_key=GOOGLE_API_KEY)
        for chunk in client.models.generate_content_stream(
            model='gemini-2.5-flash-lite',
            contents=prompt,
        ):
            yield chunk.text

    async def process_text_message(self, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Process a text message and demonstrate various task states."""
        print(f"Processing text message: {message}")
        
        # Simulate task progression through different states
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': f"Starting to process: {message}",
            'task_state': 'working'
        }
        
        await asyncio.sleep(0.5)  # Simulate processing time
        
        # Generate LLM response
        response = ''
        for chunk in self.call_llm(f"Please provide a helpful response to: {message}"):
            response += chunk
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': chunk,
                'task_state': 'working'
            }
        
        yield {
            'is_task_complete': True,
            'require_user_input': False,
            'content': f"Final response: {response}",
            'task_state': 'completed'
        }

    async def process_file_message(self, file_content: str, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Process a file message and demonstrate file handling."""
        print(f"Processing file with message: {message}")
        
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': f"Analyzing file content...",
            'task_state': 'working'
        }
        
        await asyncio.sleep(0.5)
        
        # Analyze file content
        analysis_prompt = f"""
        Please analyze this file content and provide insights:
        
        File content:
        {file_content}
        
        User request: {message}
        """
        
        response = ''
        for chunk in self.call_llm(analysis_prompt):
            response += chunk
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': chunk,
                'task_state': 'working'
            }
        
        yield {
            'is_task_complete': True,
            'require_user_input': False,
            'content': f"File analysis complete: {response}",
            'task_state': 'completed'
        }

    async def process_structured_data(self, data: Dict[str, Any], message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Process structured data and demonstrate form handling."""
        print(f"Processing structured data: {data}")
        
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': f"Processing form data...",
            'task_state': 'working'
        }
        
        await asyncio.sleep(0.5)
        
        # Process structured data
        data_analysis = f"""
        Form data received:
        {json.dumps(data, indent=2)}
        
        User request: {message}
        """
        
        response = ''
        for chunk in self.call_llm(f"Please process this form data: {data_analysis}"):
            response += chunk
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': chunk,
                'task_state': 'working'
            }
        
        yield {
            'is_task_complete': True,
            'require_user_input': False,
            'content': f"Form processing complete: {response}",
            'task_state': 'completed'
        }

    async def demonstrate_input_required(self, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Demonstrate input-required state."""
        print(f"Demonstrating input required for: {message}")
        
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': f"Processing your request: {message}",
            'task_state': 'working'
        }
        
        await asyncio.sleep(0.5)
        
        # Request additional input
        yield {
            'is_task_complete': False,
            'require_user_input': True,
            'content': "I need additional information to complete this task. Please provide: 1) Your preferred timezone, 2) Your budget range, 3) Any specific requirements.",
            'task_state': 'input-required'
        }

    async def demonstrate_long_running_task(self, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Demonstrate a long-running task with progress updates."""
        print(f"Demonstrating long-running task: {message}")
        
        steps = [
            "Initializing task...",
            "Gathering information...",
            "Processing data...",
            "Analyzing results...",
            "Generating report...",
            "Finalizing output..."
        ]
        
        for i, step in enumerate(steps):
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': f"Step {i+1}/{len(steps)}: {step}",
                'task_state': 'working'
            }
            await asyncio.sleep(1)  # Simulate processing time
        
        # Generate final response
        response = ''
        for chunk in self.call_llm(f"Please provide a comprehensive response to: {message}"):
            response += chunk
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': chunk,
                'task_state': 'working'
            }
        
        yield {
            'is_task_complete': True,
            'require_user_input': False,
            'content': f"Long-running task completed: {response}",
            'task_state': 'completed'
        }

    async def demonstrate_error_scenario(self, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Demonstrate error handling and failed state."""
        print(f"Demonstrating error scenario: {message}")
        
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': f"Starting to process: {message}",
            'task_state': 'working'
        }
        
        await asyncio.sleep(0.5)
        
        # Simulate an error
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': "Encountered an error while processing the request. The requested service is temporarily unavailable.",
            'task_state': 'failed'
        }

    async def demonstrate_cancellation_scenario(self, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Demonstrate task cancellation."""
        print(f"Demonstrating cancellation scenario: {message}")
        
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': f"Starting to process: {message}",
            'task_state': 'working'
        }
        
        await asyncio.sleep(0.5)
        
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': "Task is being processed...",
            'task_state': 'working'
        }
        
        await asyncio.sleep(0.5)
        
        # Simulate cancellation
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': "Task has been cancelled by the user.",
            'task_state': 'canceled'
        }

    async def stream(self, question: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Main streaming method that routes to different demonstration scenarios."""
        print(f"Enhanced agent processing: {question}")
        
        # Determine which demonstration to run based on the question
        question_lower = question.lower()
        
        if "error" in question_lower or "fail" in question_lower:
            async for event in self.demonstrate_error_scenario(question):
                yield event
        elif "cancel" in question_lower or "stop" in question_lower:
            async for event in self.demonstrate_cancellation_scenario(question):
                yield event
        elif "input" in question_lower or "require" in question_lower:
            async for event in self.demonstrate_input_required(question):
                yield event
        elif "long" in question_lower or "progress" in question_lower:
            async for event in self.demonstrate_long_running_task(question):
                yield event
        elif "file" in question_lower:
            # Simulate file processing
            file_content = "This is a sample file content for demonstration purposes."
            async for event in self.process_file_message(file_content, question):
                yield event
        elif "form" in question_lower or "data" in question_lower:
            # Simulate structured data processing
            form_data = {
                "name": "Demo User",
                "email": "demo@example.com",
                "preferences": ["option1", "option2"]
            }
            async for event in self.process_structured_data(form_data, question):
                yield event
        else:
            # Default text processing
            async for event in self.process_text_message(question):
                yield event


if __name__ == '__main__':
    agent = EnhancedAgent(
        token_stream_callback=lambda token: print(token, end='', flush=True),
    )

    async def main():
        """Main function."""
        async for chunk in agent.stream('What is A2A Protocol?'):
            print(chunk)

    asyncio.run(main()) 
