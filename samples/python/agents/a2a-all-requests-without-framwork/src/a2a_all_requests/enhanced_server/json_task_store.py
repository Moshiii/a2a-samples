"""
JSON-based Task Store for Enhanced A2A Server.

This module provides a simple JSON file-based task storage system
for the enhanced A2A protocol demo.
"""

import json
import os
import asyncio
from typing import Dict, Optional, List
from datetime import datetime
from a2a.types import Task, TaskState, TaskStatus


class JSONTaskStore:
    """A simple JSON file-based task store for the enhanced A2A demo.
    
    This class provides the same interface as the A2A SDK's InMemoryTaskStore:
    - save(task): Save a task to storage
    - get(task_id): Retrieve a task by ID
    - delete(task_id): Delete a task by ID
    
    Additional methods for JSON file management:
    - list_tasks(): List all task IDs
    - clear_all_tasks(): Clear all tasks
    - update_task_status(): Update a task's status
    """
    
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path
        self._lock = asyncio.Lock()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the JSON file exists with proper structure."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"tasks": {}}, f, indent=2)
    
    async def save(self, task: Task) -> None:
        """Save a task to the JSON file (aligned with A2A SDK InMemoryTaskStore)."""
        async with self._lock:
            try:
                # Load existing tasks
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                
                # Convert task to dict for storage
                task_dict = {
                    "id": task.id,
                    "context_id": getattr(task, 'context_id', ""),  # Store context_id
                    "status": {
                        "state": task.status.state.value if task.status.state else "submitted",
                        "message": task.status.message if task.status else "",
                        "final": getattr(task.status, 'final', False)  # Use getattr to safely access final
                    },
                    "artifacts": [
                        {
                            "id": artifact.id,
                            "name": artifact.name,
                            "type": artifact.type,
                            "data": artifact.data if hasattr(artifact, 'data') else None
                        }
                        for artifact in (task.artifacts or [])
                    ],
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                # Store the task
                data["tasks"][task.id] = task_dict
                
                # Save back to file
                with open(self.file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"💾 Stored task {task.id} in JSON file")
                
            except Exception as e:
                print(f"❌ Error storing task {task.id}: {e}")
                raise
    
    async def get(self, task_id: str) -> Optional[Task]:
        """Get a task from the JSON file (aligned with A2A SDK InMemoryTaskStore)."""
        async with self._lock:
            try:
                # Load tasks from file
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                
                if task_id not in data["tasks"]:
                    print(f"🔍 Task {task_id} not found in JSON store")
                    return None
                
                task_dict = data["tasks"][task_id]
                
                # Reconstruct task object
                task = Task(
                    id=task_dict["id"],
                    context_id=task_dict.get("context_id", ""),  # Add context_id
                    status=TaskStatus(
                        state=TaskState(task_dict["status"]["state"]),
                        message=task_dict["status"]["message"],
                        final=task_dict["status"]["final"]
                    ),
                    artifacts=[]  # Simplified for demo
                )
                
                print(f"📋 Retrieved task {task_id} from JSON store")
                return task
                
            except Exception as e:
                print(f"❌ Error retrieving task {task_id}: {e}")
                return None
    
    async def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update a task's status in the JSON file."""
        async with self._lock:
            try:
                # Load existing tasks
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                
                if task_id not in data["tasks"]:
                    print(f"❌ Task {task_id} not found for status update")
                    return False
                
                # Update status
                data["tasks"][task_id]["status"] = {
                    "state": status.state.value,
                    "message": status.message,
                    "final": getattr(status, 'final', False)  # Use getattr to safely access final
                }
                data["tasks"][task_id]["updated_at"] = datetime.now().isoformat()
                
                # Save back to file
                with open(self.file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"🔄 Updated task {task_id} status to {status.state.value}")
                return True
                
            except Exception as e:
                print(f"❌ Error updating task {task_id} status: {e}")
                return False
    
    async def delete(self, task_id: str) -> bool:
        """Delete a task from the JSON file (aligned with A2A SDK InMemoryTaskStore)."""
        async with self._lock:
            try:
                # Load existing tasks
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                
                if task_id not in data["tasks"]:
                    print(f"❌ Task {task_id} not found for deletion")
                    return False
                
                # Remove task
                del data["tasks"][task_id]
                
                # Save back to file
                with open(self.file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"🗑️ Deleted task {task_id} from JSON store")
                return True
                
            except Exception as e:
                print(f"❌ Error deleting task {task_id}: {e}")
                return False
    
    async def list_tasks(self) -> List[str]:
        """List all task IDs in the store."""
        async with self._lock:
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                
                task_ids = list(data["tasks"].keys())
                print(f"📋 Found {len(task_ids)} tasks in JSON store")
                return task_ids
                
            except Exception as e:
                print(f"❌ Error listing tasks: {e}")
                return []
    
    async def clear_all_tasks(self) -> None:
        """Clear all tasks from the store."""
        async with self._lock:
            try:
                with open(self.file_path, 'w') as f:
                    json.dump({"tasks": {}}, f, indent=2)
                
                print(f"🧹 Cleared all tasks from JSON store")
                
            except Exception as e:
                print(f"❌ Error clearing tasks: {e}") 
