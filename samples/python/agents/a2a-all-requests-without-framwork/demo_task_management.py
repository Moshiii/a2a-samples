#!/usr/bin/env python3
"""
Task Management Demo Script

This script demonstrates the task management capabilities of the enhanced A2A demo.
It shows how tasks are stored, retrieved, and managed using the JSON task store.
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

# Add the src directory to the Python path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from a2a_all_requests.enhanced_server.json_task_store import JSONTaskStore


async def demo_task_management():
    """Demonstrate task management capabilities."""
    
    print("🎯 Task Management Demo")
    print("=" * 50)
    
    # Initialize the task store
    task_store = JSONTaskStore("demo_tasks.json")
    
    # Clear any existing tasks for this demo
    await task_store.clear_all_tasks()
    print("🧹 Cleared existing tasks for demo")
    
    # List tasks (should be empty)
    tasks = await task_store.list_tasks()
    print(f"📋 Current tasks: {len(tasks)}")
    
    # Create some sample tasks
    from a2a.types import Task, TaskStatus, TaskState
    
    print("\n📝 Creating sample tasks...")
    
    # Task 1: Basic task
    task1 = Task(
        id="demo-task-001",
        context_id="context-001",
        status=TaskStatus(state=TaskState.submitted),
        artifacts=[]
    )
    await task_store.save(task1)
    print(f"✅ Created task: {task1.id}")
    
    # Task 2: Working task
    task2 = Task(
        id="demo-task-002",
        context_id="context-002",
        status=TaskStatus(state=TaskState.working),
        artifacts=[]
    )
    await task_store.save(task2)
    print(f"✅ Created task: {task2.id}")
    
    # Task 3: Completed task
    task3 = Task(
        id="demo-task-003",
        context_id="context-003",
        status=TaskStatus(state=TaskState.completed),
        artifacts=[]
    )
    await task_store.save(task3)
    print(f"✅ Created task: {task3.id}")
    
    # List all tasks
    print(f"\n📋 All tasks ({len(await task_store.list_tasks())}):")
    for task_id in await task_store.list_tasks():
        print(f"   - {task_id}")
    
    # Retrieve and display task details
    print(f"\n🔍 Task details:")
    for task_id in await task_store.list_tasks():
        task = await task_store.get(task_id)
        if task:
            print(f"   📋 {task.id}: {task.status.state.value}")
    
    # Update task status
    print(f"\n🔄 Updating task status...")
    new_status = TaskStatus(state=TaskState.canceled)
    success = await task_store.update_task_status("demo-task-002", new_status)
    if success:
        print("✅ Updated demo-task-002 to canceled")
    
    # Retrieve updated task
    updated_task = await task_store.get("demo-task-002")
    if updated_task:
        print(f"   📋 {updated_task.id}: {updated_task.status.state.value}")
    
    # Delete a task
    print(f"\n🗑️ Deleting task...")
    success = await task_store.delete("demo-task-003")
    if success:
        print("✅ Deleted demo-task-003")
    
    # List remaining tasks
    print(f"\n📋 Remaining tasks ({len(await task_store.list_tasks())}):")
    for task_id in await task_store.list_tasks():
        task = await task_store.get(task_id)
        if task:
            print(f"   📋 {task.id}: {task.status.state.value}")
    
    # Show JSON file contents
    print(f"\n💾 JSON file contents:")
    if os.path.exists("demo_tasks.json"):
        with open("demo_tasks.json", "r") as f:
            data = json.load(f)
            print(json.dumps(data, indent=2))
    
    print(f"\n🎉 Task management demo completed!")


if __name__ == "__main__":
    asyncio.run(demo_task_management()) 
