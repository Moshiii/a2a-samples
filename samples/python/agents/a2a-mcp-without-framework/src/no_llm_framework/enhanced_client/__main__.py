"""
Enhanced A2A Client Demo - Main Entry Point

This script demonstrates all A2A protocol communication types and features.
Run this to see a comprehensive demonstration of the A2A protocol.
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path to import the enhanced client
sys.path.append(str(Path(__file__).parent))

from enhanced_client import EnhancedA2AClient


async def run_individual_demos():
    """Run individual demonstrations of specific A2A features."""
    agent_url = "http://localhost:9999"
    
    async with EnhancedA2AClient(agent_url) as client:
        print("\n🎯 Running Individual Feature Demonstrations")
        print("=" * 60)
        
        # 1. Basic text processing
        print("\n1️⃣ Basic Text Processing Demo")
        await client.demonstrate_synchronous_message_send(
            "What is A2A protocol?"
        )
        
        # 2. Streaming demonstration
        print("\n2️⃣ Streaming Response Demo")
        await client.demonstrate_streaming_message_send(
            "Explain the benefits of agent communication"
        )
        
        # 3. File upload demonstration
        print("\n3️⃣ File Upload Demo")
        # Create a demo file
        demo_file = Path("demo_upload.txt")
        demo_file.write_text("This is a demo file for A2A protocol testing.\nIt contains sample content to demonstrate file handling capabilities.")
        
        await client.demonstrate_file_upload(
            str(demo_file), 
            "Please analyze this file and provide insights"
        )
        
        # Cleanup
        if demo_file.exists():
            demo_file.unlink()
        
        # 4. Structured data demonstration
        print("\n4️⃣ Structured Data Demo")
        form_data = {
            "user_info": {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30
            },
            "preferences": {
                "theme": "dark",
                "language": "en",
                "notifications": True
            },
            "requirements": [
                "feature1",
                "feature2",
                "feature3"
            ]
        }
        await client.demonstrate_structured_data(form_data)
        
        # 5. Task query demonstration
        print("\n5️⃣ Task Query Demo")
        # First create a task
        task_id = await client.demonstrate_synchronous_message_send(
            "Create a simple task for querying"
        )
        # Then query it
        await client.demonstrate_task_query(task_id)
        
        # 6. Push notification demonstration
        print("\n6️⃣ Push Notification Demo")
        await client.demonstrate_push_notifications(
            task_id, 
            "https://webhook.site/demo-endpoint"
        )
        
        # 7. Error handling demonstration
        print("\n7️⃣ Error Handling Demo")
        await client.demonstrate_error_handling()
        
        # 8. Task cancellation demonstration
        print("\n8️⃣ Task Cancellation Demo")
        cancel_task_id = await client.demonstrate_synchronous_message_send(
            "This task will be cancelled for demonstration"
        )
        await asyncio.sleep(1)  # Give it time to start
        await client.demonstrate_task_cancellation(cancel_task_id)


async def run_special_scenarios():
    """Run special scenarios that demonstrate specific A2A features."""
    agent_url = "http://localhost:9999"
    
    async with EnhancedA2AClient(agent_url) as client:
        print("\n🎭 Running Special Scenario Demonstrations")
        print("=" * 60)
        
        # 1. Long-running task with progress updates
        print("\n🔄 Long-running Task Demo")
        await client.demonstrate_streaming_message_send(
            "Run a long task with progress updates"
        )
        
        # 2. Input required scenario
        print("\n🤔 Input Required Demo")
        await client.demonstrate_streaming_message_send(
            "Request additional input from user"
        )
        
        # 3. Error scenario
        print("\n🚨 Error Scenario Demo")
        await client.demonstrate_streaming_message_send(
            "Demonstrate an error scenario"
        )
        
        # 4. File processing scenario
        print("\n📁 File Processing Demo")
        demo_file = Path("analysis_file.txt")
        demo_file.write_text("""
A2A Protocol Analysis Document

This document contains information about the Agent-to-Agent protocol:

1. Communication Methods:
   - message/send: Synchronous message sending
   - message/stream: Streaming message sending
   - tasks/get: Task status queries
   - tasks/cancel: Task cancellation

2. Content Types:
   - TextPart: Text content
   - FilePart: File content
   - DataPart: Structured data

3. Task States:
   - submitted: Task received
   - working: Task processing
   - input-required: Needs user input
   - completed: Task finished
   - canceled: Task cancelled
   - failed: Task failed

4. Event Types:
   - TaskStatusUpdateEvent: Status changes
   - TaskArtifactUpdateEvent: Artifact updates
        """)
        
        await client.demonstrate_file_upload(
            str(demo_file), 
            "Analyze this document and extract key information about A2A protocol"
        )
        
        # Cleanup
        if demo_file.exists():
            demo_file.unlink()
        
        # 5. Form processing scenario
        print("\n📋 Form Processing Demo")
        complex_form_data = {
            "application": {
                "type": "A2A Protocol Demo",
                "version": "2.0.0",
                "features": [
                    "streaming",
                    "push_notifications", 
                    "file_handling",
                    "structured_data",
                    "error_handling",
                    "task_cancellation"
                ]
            },
            "user": {
                "name": "Demo User",
                "role": "Developer",
                "experience": "Advanced"
            },
            "requirements": {
                "protocol_support": True,
                "streaming": True,
                "file_upload": True,
                "error_handling": True
            }
        }
        await client.demonstrate_structured_data(complex_form_data)


async def run_comprehensive_demo():
    """Run the comprehensive demonstration of all A2A protocol features."""
    agent_url = "http://localhost:9999"
    
    async with EnhancedA2AClient(agent_url) as client:
        print("\n🌟 Running Comprehensive A2A Protocol Demo")
        print("=" * 60)
        await client.run_comprehensive_demo()


async def main():
    """Main function to run the enhanced A2A client demonstrations."""
    print("🚀 Enhanced A2A Protocol Client Demo")
    print("=" * 60)
    print("This demo showcases ALL A2A protocol communication types:")
    print("• All RPC methods (message/send, message/stream, tasks/get, tasks/cancel)")
    print("• All task states (submitted, working, input-required, completed, canceled, failed)")
    print("• All event types (TaskStatusUpdateEvent, TaskArtifactUpdateEvent)")
    print("• All content types (TextPart, FilePart, DataPart)")
    print("• Push notifications")
    print("• Error handling")
    print("• Streaming responses")
    print("• Long-running tasks with progress updates")
    print("• Input requirements and user interaction")
    print("• Task cancellation")
    print("=" * 60)
    
    try:
        # Run comprehensive demo
        await run_comprehensive_demo()
        
        # Run individual feature demos
        await run_individual_demos()
        
        # Run special scenarios
        await run_special_scenarios()
        
        print("\n🎉 All A2A Protocol Demonstrations Completed Successfully!")
        print("=" * 60)
        print("✨ You have now seen demonstrations of:")
        print("   ✅ All RPC methods")
        print("   ✅ All task states")
        print("   ✅ All event types")
        print("   ✅ All content types")
        print("   ✅ Push notifications")
        print("   ✅ Error handling")
        print("   ✅ Streaming responses")
        print("   ✅ Long-running tasks")
        print("   ✅ Input requirements")
        print("   ✅ Task cancellation")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("Make sure the enhanced A2A server is running on http://localhost:9999")
        print("Run: python -m no_llm_framework.enhanced_server.__main__")


if __name__ == "__main__":
    asyncio.run(main()) 
