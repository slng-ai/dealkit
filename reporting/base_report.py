from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class BaseReport(ABC):
    def __init__(self):
        self.report_type = self.__class__.__name__.replace('Report', '')
        self.FACT_BASED_ONLY = True  # All reports must use only verified data
    
    @abstractmethod
    def generate(self, context: Dict[str, Any]) -> str:
        """Generate role-specific report from context data"""
        pass
    
    def format_unknown(self, label: str) -> str:
        """Format unknown/missing data consistently"""
        return f"- **{label}:** Not yet captured\n"
    
    def format_action_required(self, action: str, reason: str) -> str:
        """Format action items respectfully"""
        return f"- **Suggested Action:** {action}\n  - **Rationale:** {reason}\n"
    
    def format_header(self, context: Dict[str, Any]) -> str:
        """Common header for all reports"""
        customer_id = context.get('customer_id', 'Unknown')
        company_name = context.get('company_name', customer_id)
        generated_at = context.get('generated_at', datetime.now().isoformat())
        
        header = f"# {self.report_type} Report: {company_name}\n\n"
        header += f"**Customer ID:** {customer_id}\n"
        header += f"**Generated:** {generated_at.split('T')[0]}\n\n"
        
        return header
    
    def format_section(self, title: str, content: str) -> str:
        """Format a report section"""
        return f"## {title}\n\n{content}\n\n"
    
    def format_metric(self, label: str, value: Any, emoji: str = "") -> str:
        """Format a single metric line"""
        if emoji:
            return f"- {emoji} **{label}:** {value}\n"
        return f"- **{label}:** {value}\n"
    
    def calculate_engagement_score(self, context: Dict[str, Any]) -> int:
        """Calculate overall engagement score"""
        score = 0
        
        # Email activity
        email_threads = context.get('summary', {}).get('email_activity', {}).get('total_threads', 0)
        score += min(email_threads * 2, 20)
        
        # Slack activity
        slack_messages = context.get('summary', {}).get('slack_activity', {}).get('total_messages', 0)
        score += min(slack_messages // 5, 20)
        
        # Call activity
        total_calls = context.get('summary', {}).get('call_activity', {}).get('total_calls', 0)
        score += min(total_calls * 10, 30)
        
        # Meeting notes
        total_notes = context.get('summary', {}).get('meeting_notes', {}).get('total_notes', 0)
        score += min(total_notes * 5, 20)
        
        # Action items
        action_items = len(context.get('action_items', []))
        score += min(action_items * 2, 10)
        
        return min(score, 100)