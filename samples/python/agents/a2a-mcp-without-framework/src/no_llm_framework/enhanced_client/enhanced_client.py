"""
Enhanced A2A Client demonstrating all protocol communication types.

This client demonstrates:
1. All RPC methods (message/send, message/stream, tasks/get, tasks/cancel, etc.)
2. All task states (submitted, working, input-required, completed, canceled, failed)
3. All event types (TaskStatusUpdateEvent, TaskArtifactUpdateEvent)
4. All content types (TextPart, FilePart, DataPart)
5. Push notifications
6. Error handling
7. Streaming responses
"""

import asyncio
import base64
import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    DataPart,
    FilePart,
    FileWithBytes,
    Message,
    MessageSendParams,
    Part,
    PushNotificationConfig,
    Role,
    SendStreamingMessageRequest,
    SendStreamingMessageSuccessResponse,
    TaskArtifactUpdateEvent,
    TaskIdParams,
    TaskPushNotificationConfig,
    TaskQueryParams,
    TaskStatusUpdateEvent,
    TextPart,
)


class EnhancedA2AClient:
    """Enhanced A2A Client demonstrating all protocol features."""

    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.agent_card: Optional[AgentCard] = None
        self.httpx_client: Optional[httpx.AsyncClient] = None
        self.a2a_client: Optional[A2AClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.httpx_client = httpx.AsyncClient(timeout=30.0)
        await self._fetch_agent_card()
        self.a2a_client = A2AClient(self.httpx_client, agent_card=self.agent_card)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.httpx_client:
            await self.httpx_client.aclose()

    async def _fetch_agent_card(self):
        """Fetch the agent card from the server."""
        if not self.httpx_client:
            raise RuntimeError("HTTP client not initialized")
        
        response = await self.httpx_client.get(f"{self.agent_url}/.well-known/agent.json")
        response.raise_for_status()
        self.agent_card = AgentCard(**response.json())
        print(f"📋 Agent Card: {self.agent_card.name} - {self.agent_card.description}")

    async def demonstrate_synchronous_message_send(self, message_text: str) -> str:
        """Demonstrate synchronous message/send method."""
        print("\n🔄 Demonstrating synchronous message/send...")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        task_id = str(uuid.uuid4())
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text=message_text))],
            message_id=str(uuid.uuid4()),
            task_id=task_id,
        )

        params = MessageSendParams(message=message)
        
        try:
            response = await self.a2a_client.send_message(params)
            print(f"✅ Synchronous response received for task {task_id}")
            print(f"   Status: {response.status.state}")
            if response.artifacts:
                for artifact in response.artifacts:
                    print(f"   Artifact: {artifact.name} - {artifact.description}")
            return task_id
        except Exception as e:
            print(f"❌ Error in synchronous send: {e}")
            return task_id

    async def demonstrate_streaming_message_send(self, message_text: str) -> str:
        """Demonstrate streaming message/stream method."""
        print("\n🌊 Demonstrating streaming message/stream...")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        task_id = str(uuid.uuid4())
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text=message_text))],
            message_id=str(uuid.uuid4()),
            task_id=task_id,
        )

        params = MessageSendParams(message=message)
        streaming_request = SendStreamingMessageRequest(
            id=str(uuid.uuid4()), params=params
        )

        try:
            async for chunk in self.a2a_client.send_message_streaming(streaming_request):
                if isinstance(chunk.root, SendStreamingMessageSuccessResponse):
                    result = chunk.root.result
                    if isinstance(result, TaskStatusUpdateEvent):
                        print(f"📊 Status Update: {result.status.state}")
                        if result.status.message:
                            for part in result.status.message.parts:
                                if hasattr(part.root, 'text'):
                                    print(f"   Message: {part.root.text}")
                    elif isinstance(result, TaskArtifactUpdateEvent):
                        print(f"📎 Artifact Update: {result.artifact.name}")
                        for part in result.artifact.parts:
                            if hasattr(part.root, 'text'):
                                print(f"   Content: {part.root.text}")
            print(f"✅ Streaming completed for task {task_id}")
            return task_id
        except Exception as e:
            print(f"❌ Error in streaming send: {e}")
            return task_id

    async def demonstrate_file_upload(self, file_path: str, message_text: str) -> str:
        """Demonstrate file upload with FilePart."""
        print(f"\n📁 Demonstrating file upload: {file_path}")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        # Read and encode file
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            print(f"❌ File not found: {file_path}")
            return ""

        with open(file_path_obj, 'rb') as f:
            file_content = f.read()
            file_base64 = base64.b64encode(file_content).decode('utf-8')

        task_id = str(uuid.uuid4())
        
        # Create message with both text and file parts
        text_part = Part(root=TextPart(text=message_text))
        file_part = Part(
            root=FilePart(
                file=FileWithBytes(
                    name=file_path_obj.name,
                    mime_type="text/plain",
                    bytes=file_base64
                )
            )
        )

        message = Message(
            role=Role.user,
            parts=[text_part, file_part],
            message_id=str(uuid.uuid4()),
            task_id=task_id,
        )

        params = MessageSendParams(message=message)
        
        try:
            response = await self.a2a_client.send_message(params)
            print(f"✅ File upload completed for task {task_id}")
            print(f"   Status: {response.status.state}")
            return task_id
        except Exception as e:
            print(f"❌ Error in file upload: {e}")
            return task_id

    async def demonstrate_structured_data(self, form_data: Dict[str, Any]) -> str:
        """Demonstrate structured data with DataPart."""
        print(f"\n📋 Demonstrating structured data: {form_data}")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        task_id = str(uuid.uuid4())
        
        # Create message with structured data
        data_part = Part(root=DataPart(data=form_data))
        text_part = Part(root=TextPart(text="Please process this form data"))

        message = Message(
            role=Role.user,
            parts=[text_part, data_part],
            message_id=str(uuid.uuid4()),
            task_id=task_id,
        )

        params = MessageSendParams(message=message)
        
        try:
            response = await self.a2a_client.send_message(params)
            print(f"✅ Structured data sent for task {task_id}")
            print(f"   Status: {response.status.state}")
            return task_id
        except Exception as e:
            print(f"❌ Error in structured data: {e}")
            return task_id

    async def demonstrate_task_query(self, task_id: str):
        """Demonstrate tasks/get method."""
        print(f"\n🔍 Demonstrating task query for: {task_id}")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        params = TaskQueryParams(id=task_id)
        
        try:
            response = await self.a2a_client.get_task(params)
            print(f"✅ Task query successful")
            print(f"   Task ID: {response.id}")
            print(f"   Status: {response.status.state}")
            if response.artifacts:
                print(f"   Artifacts: {len(response.artifacts)}")
            return response
        except Exception as e:
            print(f"❌ Error in task query: {e}")
            return None

    async def demonstrate_task_cancellation(self, task_id: str):
        """Demonstrate tasks/cancel method."""
        print(f"\n⏹️ Demonstrating task cancellation for: {task_id}")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        params = TaskIdParams(id=task_id)
        
        try:
            response = await self.a2a_client.cancel_task(params)
            print(f"✅ Task cancellation successful")
            print(f"   Task ID: {response.id}")
            print(f"   Status: {response.status.state}")
            return response
        except Exception as e:
            print(f"❌ Error in task cancellation: {e}")
            return None

    async def demonstrate_push_notifications(self, task_id: str, webhook_url: str):
        """Demonstrate push notification setup."""
        print(f"\n🔔 Demonstrating push notification setup for: {task_id}")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        # Set push notification config
        push_config = PushNotificationConfig(
            url=webhook_url,
            token="demo-token-123",
            authentication=None
        )
        
        set_params = TaskPushNotificationConfig(
            id=task_id,
            push_notification=push_config
        )
        
        try:
            # Set push notification
            response = await self.a2a_client.set_task_push_notification(set_params)
            print(f"✅ Push notification set successfully")
            print(f"   Webhook URL: {response.push_notification.url}")
            
            # Get push notification config
            get_params = TaskIdParams(id=task_id)
            get_response = await self.a2a_client.get_task_push_notification(get_params)
            print(f"✅ Push notification config retrieved")
            print(f"   Token: {get_response.push_notification.token}")
            
            return response
        except Exception as e:
            print(f"❌ Error in push notification setup: {e}")
            return None

    async def demonstrate_error_handling(self):
        """Demonstrate various error scenarios."""
        print("\n🚨 Demonstrating error handling...")
        
        if not self.a2a_client:
            raise RuntimeError("A2A client not initialized")

        # Test with invalid task ID
        print("   Testing invalid task ID...")
        try:
            params = TaskQueryParams(id="invalid-task-id")
            await self.a2a_client.get_task(params)
        except Exception as e:
            print(f"   ✅ Expected error caught: {type(e).__name__}")

        # Test with invalid message
        print("   Testing invalid message...")
        try:
            message = Message(
                role=Role.user,
                parts=[],  # Empty parts should cause error
                message_id=str(uuid.uuid4()),
                task_id=str(uuid.uuid4()),
            )
            params = MessageSendParams(message=message)
            await self.a2a_client.send_message(params)
        except Exception as e:
            print(f"   ✅ Expected error caught: {type(e).__name__}")

    async def run_comprehensive_demo(self):
        """Run a comprehensive demonstration of all A2A protocol features."""
        print("🚀 Starting Comprehensive A2A Protocol Demo")
        print("=" * 50)

        # 1. Synchronous message sending
        sync_task_id = await self.demonstrate_synchronous_message_send(
            "Hello! This is a synchronous message test."
        )

        # 2. Streaming message sending
        stream_task_id = await self.demonstrate_streaming_message_send(
            "Hello! This is a streaming message test."
        )

        # 3. File upload demonstration
        # Create a temporary file for demo
        demo_file = Path("demo_file.txt")
        demo_file.write_text("This is a demo file content for A2A protocol testing.")
        
        file_task_id = await self.demonstrate_file_upload(
            str(demo_file), 
            "Please analyze this file content."
        )

        # 4. Structured data demonstration
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "preferences": ["option1", "option2"]
        }
        data_task_id = await self.demonstrate_structured_data(form_data)

        # 5. Task query demonstration
        await self.demonstrate_task_query(sync_task_id)

        # 6. Push notification demonstration
        await self.demonstrate_push_notifications(
            sync_task_id, 
            "https://webhook.site/demo-endpoint"
        )

        # 7. Error handling demonstration
        await self.demonstrate_error_handling()

        # 8. Task cancellation demonstration (use a new task)
        cancel_task_id = await self.demonstrate_synchronous_message_send(
            "This task will be cancelled."
        )
        # Wait a bit to ensure task is processing
        await asyncio.sleep(1)
        await self.demonstrate_task_cancellation(cancel_task_id)

        # Cleanup
        if demo_file.exists():
            demo_file.unlink()

        print("\n🎉 Comprehensive A2A Protocol Demo Completed!")
        print("=" * 50)


async def main():
    """Main function to run the enhanced A2A client demo."""
    agent_url = "http://localhost:9999"
    
    async with EnhancedA2AClient(agent_url) as client:
        await client.run_comprehensive_demo()


if __name__ == "__main__":
    asyncio.run(main()) 
