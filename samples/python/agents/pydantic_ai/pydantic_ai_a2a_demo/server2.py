import asyncio
import uvicorn
import httpx
import uuid
from pydantic_ai import Agent
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Create the second agent
agent2 = Agent(
    'openai:gpt-4o',
    instructions="""
    You are Server 2, a helpful AI assistant. You can:
    - Answer questions about various topics
    - Help with coding problems
    - Provide explanations and examples
    - Engage in casual conversation
    
    You will be communicating with Server 1. Be friendly and helpful.
    """,
    name="Server 2 Assistant"
)

# Create the FastA2A app
app2 = agent2.to_a2a(
    name="Server 2 Assistant",
    description="Second A2A server that communicates with Server 1",
    url="http://localhost:8001",
    version="1.0.0"
)

class Server2Client:
    def __init__(self, server1_url: str = "http://localhost:8000"):
        self.server1_url = server1_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def send_message_to_server1(self, message: str) -> dict:
        """Send a message to Server 1."""
        message_id = str(uuid.uuid4())
        
        payload = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": message}],
                    "kind": "message",
                    "messageId": message_id
                }
            },
            "id": message_id
        }
        
        print(f"Server 2 -> Server 1: {message}")
        response = await self.client.post(
            f"{self.server1_url}/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error from Server 1: {response.status_code}")
            return {"error": f"HTTP {response.status_code}"}
    
    async def wait_for_task_completion(self, task_id: str, max_wait: int = 30) -> dict:
        """Wait for a task to complete."""
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait:
            status_payload = {
                "jsonrpc": "2.0",
                "method": "tasks/get",
                "params": {"id": task_id},
                "id": str(uuid.uuid4())
            }
            
            response = await self.client.post(
                f"{self.server1_url}/",
                json=status_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                status = response.json()
                if "result" in status:
                    task_status = status["result"].get("status", {})
                    state = task_status.get("state", "unknown")
                    
                    if state in ["completed", "failed"]:
                        return status
                    elif state == "working":
                        print("Task is still working...")
                    else:
                        print(f"Task state: {state}")
            
            await asyncio.sleep(2)
        
        return {"error": "Task timeout"}
    
    async def extract_response_text(self, task_result: dict) -> str:
        """Extract the response text from a completed task."""
        if "result" not in task_result:
            return "No result found"
        
        result_data = task_result["result"]
        
        if result_data.get("artifacts"):
            response_parts = []
            for artifact in result_data["artifacts"]:
                for part in artifact.get("parts", []):
                    if part.get("kind") == "text":
                        response_parts.append(part["text"])
            
            return "\n".join(response_parts)
        
        return "No response content found"
    
    async def communicate_with_server1(self):
        """Start communication with Server 1."""
        print("Server 2: Starting communication with Server 1...")
        
        # Wait a bit for Server 1 to be ready
        await asyncio.sleep(5)
        
        # First message from Server 2 to Server 1
        print("\n=== Round 1: Server 2 -> Server 1 ===")
        result1 = await self.send_message_to_server1(
            "Hello Server 1! I'm Server 2. Can you tell me about artificial intelligence?"
        )
        
        if "result" in result1:
            task_id1 = result1["result"].get("id")
            if task_id1:
                print("Waiting for Server 1 response...")
                final_result1 = await self.wait_for_task_completion(task_id1)
                response1 = await self.extract_response_text(final_result1)
                print(f"Server 1 response: {response1[:200]}...")
        
        await asyncio.sleep(3)
        
        # Second message from Server 2 to Server 1
        print("\n=== Round 2: Server 2 -> Server 1 ===")
        result2 = await self.send_message_to_server1(
            "That's fascinating! Can you also explain deep learning and neural networks?"
        )
        
        if "result" in result2:
            task_id2 = result2["result"].get("id")
            if task_id2:
                print("Waiting for Server 1 response...")
                final_result2 = await self.wait_for_task_completion(task_id2)
                response2 = await self.extract_response_text(final_result2)
                print(f"Server 1 response: {response2[:200]}...")
        
        await asyncio.sleep(3)
        
        # Third message from Server 2 to Server 1
        print("\n=== Round 3: Server 2 -> Server 1 ===")
        result3 = await self.send_message_to_server1(
            "Thank you! Can you also explain the difference between supervised and unsupervised learning?"
        )
        
        if "result" in result3:
            task_id3 = result3["result"].get("id")
            if task_id3:
                print("Waiting for Server 1 response...")
                final_result3 = await self.wait_for_task_completion(task_id3)
                response3 = await self.extract_response_text(final_result3)
                print(f"Server 1 response: {response3[:200]}...")
        
        await self.client.aclose()
        print("\nServer 2: Communication completed!")

async def start_server2():
    """Start Server 2 and begin communication."""
    # Start the server in the background
    config = uvicorn.Config(app2, host="0.0.0.0", port=8001, log_level="info")
    server = uvicorn.Server(config)
    
    # Start server in background
    server_task = asyncio.create_task(server.serve())
    
    # Wait a moment for server to start
    await asyncio.sleep(2)
    print("Server 2 started on http://localhost:8001")
    
    # Start communication
    client = Server2Client()
    await client.communicate_with_server1()
    
    # Stop the server
    server.should_exit = True
    await server_task

if __name__ == "__main__":
    print("Starting Server 2...")
    asyncio.run(start_server2()) 