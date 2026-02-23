"""
SocialHook-X - Threading Engine Module

Provides high-performance multithreading for parallel credential capture,
database operations, and concurrent request handling.
"""

import threading
import logging
import queue
import time
from typing import Callable, Any, List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


@dataclass
class ThreadTask:
    """Represents a threading task"""
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


class ThreadingEngine:
    """High-performance threading engine for parallel operations"""
    
    def __init__(self, max_workers: int = 10):
        """Initialize threading engine
        
        Args:
            max_workers: Maximum worker threads (default: 10)
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, ThreadTask] = {}
        self.task_queue: queue.Queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = False
    
    def _execute_task(self, task: ThreadTask) -> None:
        """Execute task in thread
        
        Args:
            task: ThreadTask to execute
        """
        try:
            task.status = "running"
            task.started_at = datetime.now()
            logger.info(f"Starting thread task: {task.name} (ID: {task.task_id})")
            
            # Execute callback
            task.result = task.callback(*task.args, **task.kwargs)
            
            task.status = "completed"
            task.completed_at = datetime.now()
            duration = (task.completed_at - task.started_at).total_seconds()
            logger.info(f"Completed thread task: {task.name} ({duration:.2f}s)")
        
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now()
            logger.error(f"Failed thread task {task.name}: {e}")
    
    def submit(self, task: ThreadTask) -> str:
        """Submit a task for threaded execution
        
        Args:
            task: ThreadTask to execute
        
        Returns:
            Task ID
        """
        with self.lock:
            self.tasks[task.task_id] = task
        
        # Submit to executor
        future = self.executor.submit(self._execute_task, task)
        
        return task.task_id
    
    def batch_submit(self, tasks: List[ThreadTask]) -> List[str]:
        """Submit multiple tasks for parallel execution
        
        Args:
            tasks: List of ThreadTask objects
        
        Returns:
            List of task IDs
        """
        task_ids = []
        for task in tasks:
            task_ids.append(self.submit(task))
        return task_ids
    
    def wait_all(self, timeout: Optional[float] = None) -> Dict[str, ThreadTask]:
        """Wait for all tasks to complete
        
        Args:
            timeout: Timeout in seconds
        
        Returns:
            Dictionary of completed tasks
        """
        start_time = time.time()
        while True:
            with self.lock:
                pending = sum(1 for t in self.tasks.values() if t.status == "pending" or t.status == "running")
            
            if pending == 0:
                break
            
            if timeout and (time.time() - start_time) > timeout:
                logger.warning(f"Task timeout after {timeout} seconds")
                break
            
            time.sleep(0.1)
        
        return self.tasks
    
    def wait_task(self, task_id: str, timeout: Optional[float] = None) -> Optional[ThreadTask]:
        """Wait for specific task to complete
        
        Args:
            task_id: Task ID
            timeout: Timeout in seconds
        
        Returns:
            Completed task or None
        """
        start_time = time.time()
        while task_id in self.tasks:
            task = self.tasks[task_id]
            if task.status in ["completed", "failed"]:
                return task
            
            if timeout and (time.time() - start_time) > timeout:
                logger.warning(f"Task {task_id} timeout after {timeout} seconds")
                return None
            
            time.sleep(0.05)
        
        return None
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get task status
        
        Args:
            task_id: Task ID
        
        Returns:
            Task status dictionary
        """
        with self.lock:
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
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics
        
        Returns:
            Statistics dictionary
        """
        with self.lock:
            completed = sum(1 for t in self.tasks.values() if t.status == "completed")
            failed = sum(1 for t in self.tasks.values() if t.status == "failed")
            running = sum(1 for t in self.tasks.values() if t.status == "running")
            pending = sum(1 for t in self.tasks.values() if t.status == "pending")
        
        return {
            "total_tasks": len(self.tasks),
            "completed": completed,
            "failed": failed,
            "running": running,
            "pending": pending,
            "max_workers": self.max_workers
        }
    
    def clear_completed(self) -> int:
        """Clear completed tasks from memory
        
        Returns:
            Number of tasks cleared
        """
        with self.lock:
            task_ids_to_remove = [
                task_id for task_id, task in self.tasks.items()
                if task.status in ["completed", "failed"]
            ]
            
            for task_id in task_ids_to_remove:
                del self.tasks[task_id]
        
        count = len(task_ids_to_remove)
        logger.info(f"Cleared {count} completed tasks")
        return count
    
    def shutdown(self, wait: bool = True) -> None:
        """Shutdown executor
        
        Args:
            wait: Wait for pending tasks
        """
        logger.info("Shutting down threading engine")
        self.executor.shutdown(wait=wait)
        self.running = False


# Global threading engine instance
_threading_engine = None


def get_threading_engine(max_workers: int = 10) -> ThreadingEngine:
    """Get or create threading engine instance
    
    Args:
        max_workers: Maximum worker threads
    
    Returns:
        ThreadingEngine instance
    """
    global _threading_engine
    if _threading_engine is None:
        _threading_engine = ThreadingEngine(max_workers=max_workers)
    return _threading_engine


def batch_process_credentials(credentials: List[Dict], processor: Callable) -> List[Dict]:
    """Batch process credentials using threading
    
    Args:
        credentials: List of credential dictionaries
        processor: Processing function
    
    Returns:
        List of processed credentials
    """
    engine = get_threading_engine()
    tasks = []
    
    for i, cred in enumerate(credentials):
        task = ThreadTask(
            task_id=f"cred_process_{i}",
            name=f"Process credential {i}",
            callback=processor,
            kwargs={"credential": cred}
        )
        tasks.append(task)
    
    task_ids = engine.batch_submit(tasks)
    engine.wait_all(timeout=30)
    
    results = []
    for task_id in task_ids:
        task_status = engine.get_task_status(task_id)
        if task_status and task_status["status"] == "completed":
            results.append(task_status["result"])
    
    return results


def parallel_database_writes(records: List[Dict], db_writer: Callable) -> List[bool]:
    """Parallel database write operations
    
    Args:
        records: List of records to write
        db_writer: Database write function
    
    Returns:
        List of success/failure booleans
    """
    engine = get_threading_engine(max_workers=5)
    tasks = []
    
    for i, record in enumerate(records):
        task = ThreadTask(
            task_id=f"db_write_{i}",
            name=f"Write record {i}",
            callback=db_writer,
            kwargs={"record": record}
        )
        tasks.append(task)
    
    task_ids = engine.batch_submit(tasks)
    engine.wait_all(timeout=60)
    
    results = []
    for task_id in task_ids:
        task_status = engine.get_task_status(task_id)
        if task_status and task_status["status"] == "completed":
            results.append(True)
        else:
            results.append(False)
    
    return results
