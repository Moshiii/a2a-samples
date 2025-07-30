#!/usr/bin/env python3
"""
In-Memory Task Management Demo Script

This script demonstrates the task management capabilities using the A2A SDK's
built-in InMemoryTaskStore for the enhanced A2A demo.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import Task, TaskStatus, TaskState


async def demo_inmemory_task_management():
    """Demonstrate in-memory task management capabilities."""
    
    print("🎯 In-Memory Task Management Demo")
    print("=" * 50)
    
    # Initialize the in-memory task store
    task_store = InMemoryTaskStore()
    
    # Note: InMemoryTaskStore doesn't have a list_tasks method
    # We'll demonstrate the available methods: get, save, delete
    print(f"📋 InMemoryTaskStore methods: get, save, delete")
    
    # Create some sample tasks
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
    
    # Retrieve and display task details
    print(f"\n🔍 Task details:")
    task_ids = ["demo-task-001", "demo-task-002", "demo-task-003"]
    for task_id in task_ids:
        task = await task_store.get(task_id)
        if task:
            print(f"   📋 {task.id}: {task.status.state.value}")
        else:
            print(f"   ❌ {task_id}: Not found")
    
    # Update task status
    print(f"\n🔄 Updating task status...")
    new_status = TaskStatus(state=TaskState.canceled)
    task2.status = new_status
    await task_store.save(task2)
    print("✅ Updated demo-task-002 to canceled")
    
    # Retrieve updated task
    updated_task = await task_store.get("demo-task-002")
    if updated_task:
        print(f"   📋 {updated_task.id}: {updated_task.status.state.value}")
    
    # Delete a task
    print(f"\n🗑️ Deleting task...")
    await task_store.delete("demo-task-003")
    print("✅ Deleted demo-task-003")
    
    # Check remaining tasks
    print(f"\n📋 Remaining tasks:")
    remaining_task_ids = ["demo-task-001", "demo-task-002", "demo-task-003"]
    for task_id in remaining_task_ids:
        task = await task_store.get(task_id)
        if task:
            print(f"   📋 {task.id}: {task.status.state.value}")
        else:
            print(f"   ❌ {task_id}: Not found (deleted)")
    
    # Test task not found
    print(f"\n🔍 Testing task not found...")
    non_existent_task = await task_store.get("non-existent-task")
    if non_existent_task is None:
        print("✅ Correctly returned None for non-existent task")
    
    # Test concurrent access
    print(f"\n🔄 Testing concurrent access...")
    async def concurrent_task_operations():
        # Create a new task concurrently
        concurrent_task = Task(
            id="concurrent-task",
            context_id="concurrent-context",
            status=TaskStatus(state=TaskState.submitted),
            artifacts=[]
        )
        await task_store.save(concurrent_task)
        print(f"   ✅ Concurrently created task: {concurrent_task.id}")
        
        # Retrieve it concurrently
        retrieved_task = await task_store.get("concurrent-task")
        if retrieved_task:
            print(f"   ✅ Concurrently retrieved task: {retrieved_task.id}")
    
    await concurrent_task_operations()
    
    # Final task check
    print(f"\n📊 Final task check:")
    final_task_ids = ["demo-task-001", "demo-task-002", "demo-task-003", "concurrent-task"]
    for task_id in final_task_ids:
        task = await task_store.get(task_id)
        if task:
            print(f"   📋 {task.id}: {task.status.state.value}")
        else:
            print(f"   ❌ {task_id}: Not found")
    
    print(f"\n🎉 In-memory task management demo completed!")
    print(f"💡 Note: Tasks are stored in memory and will be lost when the process ends")


if __name__ == "__main__":
    asyncio.run(demo_inmemory_task_management()) 
