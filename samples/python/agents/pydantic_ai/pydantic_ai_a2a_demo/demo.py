#!/usr/bin/env python3
"""
A2A Server Communication Demo

This demo starts two A2A servers that communicate with each other.
Server 1 (Passive): Waits for messages from Server 2
Server 2 (Active): Sends messages to Server 1
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

async def run_demo():
    """Run the A2A server communication demo."""
    print("=== A2A Server Communication Demo ===")
    print("Server 1 (Passive): Will wait for messages from Server 2")
    print("Server 2 (Active): Will send messages to Server 1")
    print("Server 1: http://localhost:8000")
    print("Server 2: http://localhost:8001")
    print()
    
    # Check if the server files exist
    server1_file = Path("server1.py")
    server2_file = Path("server2.py")
    
    if not server1_file.exists():
        print("Error: server1.py not found!")
        return
    
    if not server2_file.exists():
        print("Error: server2.py not found!")
        return
    
    print("Starting Server 1 (Passive)...")
    # Start Server 1 in background
    server1_process = subprocess.Popen([
        sys.executable, "server1.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait a moment for Server 1 to start
    await asyncio.sleep(3)
    
    print("Starting Server 2 (Active)...")
    # Start Server 2 in background
    server2_process = subprocess.Popen([
        sys.executable, "server2.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for both servers to complete their communication
    print("Waiting for servers to communicate...")
    print("Server 2 will send messages to Server 1...")
    
    # Monitor the processes
    while True:
        # Check if both processes are still running
        server1_running = server1_process.poll() is None
        server2_running = server2_process.poll() is None
        
        if not server1_running and not server2_running:
            print("Both servers have completed their communication.")
            break
        
        # Print output from Server 1
        if server1_running:
            try:
                output = server1_process.stdout.readline()
                if output:
                    print(f"[Server 1] {output.strip()}")
            except:
                pass
        
        # Print output from Server 2
        if server2_running:
            try:
                output = server2_process.stdout.readline()
                if output:
                    print(f"[Server 2] {output.strip()}")
            except:
                pass
        
        await asyncio.sleep(0.1)
    
    # Get final output
    server1_stdout, server1_stderr = server1_process.communicate()
    server2_stdout, server2_stderr = server2_process.communicate()
    
    print("\n=== Demo Completed ===")
    print("Server 1 (Passive) output:")
    print(server1_stdout)
    if server1_stderr:
        print("Server 1 errors:")
        print(server1_stderr)
    
    print("\nServer 2 (Active) output:")
    print(server2_stdout)
    if server2_stderr:
        print("Server 2 errors:")
        print(server2_stderr)

def main():
    """Main function to run the demo."""
    print("A2A Server Communication Demo")
    print("Make sure you have set up your .env file with OPENAI_API_KEY")
    print()
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("Warning: .env file not found. Make sure OPENAI_API_KEY is set.")
        print()
    
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"Error running demo: {e}")

if __name__ == "__main__":
    main() 