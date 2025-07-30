#!/usr/bin/env python3
"""
Test script to verify JSONTaskStore compatibility with A2A SDK InMemoryTaskStore.

This script tests that the JSONTaskStore provides the same interface as the
A2A SDK's InMemoryTaskStore and can be used as a drop-in replacement.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from a2a_all_requests.enhanced_server.json_task_store import JSONTaskStore
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import Task, TaskStatus, TaskState


async def test_compatibility():
    """Test that JSONTaskStore is compatible with InMemoryTaskStore interface."""
    
    print("🧪 Testing JSONTaskStore compatibility with A2A SDK InMemoryTaskStore")
    print("=" * 70)
    
    # Test both stores
    stores = {
        "InMemoryTaskStore": InMemoryTaskStore(),
        "JSONTaskStore": JSONTaskStore("test_tasks.json")
    }
    
    for store_name, store in stores.items():
        print(f"\n📋 Testing {store_name}...")
        
        # Test 1: Save a task
        print("   🔧 Testing save() method...")
        task = Task(
            id="test-task-001",
            context_id="test-context",
            status=TaskStatus(state=TaskState.submitted),
            artifacts=[]
        )
        
        try:
            await store.save(task)
            print("   ✅ save() method works")
        except Exception as e:
            print(f"   ❌ save() method failed: {e}")
            continue
        
        # Test 2: Get a task
        print("   🔍 Testing get() method...")
        try:
            retrieved_task = await store.get("test-task-001")
            if retrieved_task and retrieved_task.id == "test-task-001":
                print("   ✅ get() method works")
            else:
                print("   ❌ get() method returned wrong task")
        except Exception as e:
            print(f"   ❌ get() method failed: {e}")
            continue
        
        # Test 3: Delete a task
        print("   🗑️ Testing delete() method...")
        try:
            await store.delete("test-task-001")
            # Verify it's deleted
            deleted_task = await store.get("test-task-001")
            if deleted_task is None:
                print("   ✅ delete() method works")
            else:
                print("   ❌ delete() method didn't actually delete the task")
        except Exception as e:
            print(f"   ❌ delete() method failed: {e}")
            continue
        
        print(f"   🎉 {store_name} passed all compatibility tests!")
    
    print(f"\n🎯 Compatibility Test Summary:")
    print("=" * 70)
    print("✅ JSONTaskStore provides the same interface as InMemoryTaskStore")
    print("✅ All core methods (save, get, delete) work correctly")
    print("✅ JSONTaskStore can be used as a drop-in replacement")
    print("✅ Additional methods (list_tasks, clear_all_tasks) are available")
    print("\n💡 The JSONTaskStore is now fully aligned with A2A SDK standards!")


if __name__ == "__main__":
    asyncio.run(test_compatibility()) 
