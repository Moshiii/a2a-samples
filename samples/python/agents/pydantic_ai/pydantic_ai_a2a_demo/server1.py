import asyncio
import uvicorn
from pydantic_ai import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the first agent
agent1 = Agent(
    'openai:gpt-4o',
    instructions="""
    You are Server 1, a helpful AI assistant. You can:
    - Answer questions about various topics
    - Help with coding problems
    - Provide explanations and examples
    - Engage in casual conversation
    
    You will be communicating with Server 2. Be friendly and helpful.
    """,
    name="Server 1 Assistant"
)

# Create the FastA2A app
app1 = agent1.to_a2a(
    name="Server 1 Assistant",
    description="First A2A server that communicates with Server 2",
    url="http://localhost:8000",
    version="1.0.0"
)



async def start_server1():
    """Start Server 1 and wait for Server 2 to communicate."""
    # Start the server in the background
    config = uvicorn.Config(app1, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    # Start server in background
    server_task = asyncio.create_task(server.serve())
    
    # Wait a moment for server to start
    await asyncio.sleep(2)
    print("Server 1 started on http://localhost:8000")
    print("Server 1 is waiting for Server 2 to send messages...")
    
    # Keep the server running for a while to receive messages
    try:
        await asyncio.sleep(200)  # Wait for 60 seconds
    except KeyboardInterrupt:
        print("Server 1 shutting down...")
    
    # Stop the server
    server.should_exit = True
    await server_task

if __name__ == "__main__":
    print("Starting Server 1...")
    asyncio.run(start_server1()) 