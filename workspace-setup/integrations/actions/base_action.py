"""
Base action class for trigger responses
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class ActionStatus(Enum):
    """Status of action execution"""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    SKIPPED = "skipped"


@dataclass
class ActionResult:
    """Result of executing an action"""
    status: ActionStatus
    message: str
    data: Dict[str, Any] = None
    execution_time_ms: float = 0
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "status": self.status.value,
            "message": self.message,
            "data": self.data or {},
            "execution_time_ms": self.execution_time_ms,
            "error": self.error
        }


class BaseAction(ABC):
    """Base class for all trigger actions"""
    
    def __init__(self, 
                 action_id: str,
                 name: str,
                 description: str,
                 enabled: bool = True):
        self.action_id = action_id
        self.name = name
        self.description = description
        self.enabled = enabled
        self.execution_count = 0
        self.last_executed: Optional[datetime] = None
        self.success_count = 0
        self.failure_count = 0
    
    async def execute(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """
        Execute the action with trigger data
        
        Args:
            trigger_data: Data from the trigger event
            
        Returns:
            ActionResult with execution details
        """
        if not self.enabled:
            return ActionResult(
                status=ActionStatus.SKIPPED,
                message=f"Action {self.name} is disabled"
            )
        
        start_time = datetime.now()
        
        try:
            # Execute the action implementation
            result = await self._execute_impl(trigger_data)
            
            # Update statistics
            self.execution_count += 1
            self.last_executed = start_time
            
            if result.status == ActionStatus.SUCCESS:
                self.success_count += 1
            else:
                self.failure_count += 1
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            result.execution_time_ms = execution_time
            
            return result
            
        except Exception as e:
            self.execution_count += 1
            self.failure_count += 1
            self.last_executed = start_time
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ActionResult(
                status=ActionStatus.FAILED,
                message=f"Action {self.name} failed with error",
                execution_time_ms=execution_time,
                error=str(e)
            )
    
    @abstractmethod
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """
        Implementation of the action execution
        
        Args:
            trigger_data: Data from the trigger event
            
        Returns:
            ActionResult with execution details
        """
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get action execution statistics"""
        return {
            "action_id": self.action_id,
            "name": self.name,
            "enabled": self.enabled,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": self.success_count / max(self.execution_count, 1),
            "last_executed": self.last_executed.isoformat() if self.last_executed else None
        }
    
    def reset_stats(self):
        """Reset action statistics"""
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.last_executed = None
    
    def should_execute(self, trigger_data: Dict[str, Any]) -> bool:
        """
        Check if action should execute based on trigger data
        
        Args:
            trigger_data: Data from the trigger event
            
        Returns:
            True if action should execute
        """
        # Override in subclasses for custom logic
        return self.enabled
    
    def get_recipients(self, trigger_data: Dict[str, Any]) -> list:
        """
        Get list of recipients for this action
        
        Args:
            trigger_data: Data from the trigger event
            
        Returns:
            List of recipients (emails, user IDs, etc.)
        """
        # Override in subclasses
        return []
    
    def format_message(self, trigger_data: Dict[str, Any]) -> str:
        """
        Format message content for this action
        
        Args:
            trigger_data: Data from the trigger event
            
        Returns:
            Formatted message string
        """
        # Override in subclasses
        return f"Trigger {trigger_data.get('trigger_id', 'unknown')} was activated"