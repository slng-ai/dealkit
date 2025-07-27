"""
Reporting actions for triggers
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from .base_action import BaseAction, ActionResult, ActionStatus


class AddToReportAction(BaseAction):
    """Add trigger events to daily/weekly reports"""
    
    def __init__(self,
                 action_id: str = "add_to_report",
                 name: str = "Add to Report",
                 description: str = "Include trigger events in reports",
                 report_storage_path: str = "workspace-setup/reports/trigger_events",
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.report_storage_path = Path(report_storage_path)
        self.report_storage_path.mkdir(parents=True, exist_ok=True)
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute report addition"""
        try:
            # Format trigger data for reporting
            report_entry = self._format_report_entry(trigger_data)
            
            # Add to appropriate report files
            await self._add_to_daily_report(report_entry)
            await self._add_to_weekly_report(report_entry)
            await self._add_to_customer_report(report_entry)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message="Trigger event added to reports",
                data={"report_entry": report_entry}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to add to reports",
                error=str(e)
            )
    
    def _format_report_entry(self, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format trigger data for reporting"""
        return {
            "timestamp": trigger_data.get("timestamp", datetime.now().isoformat()),
            "trigger_id": trigger_data.get("trigger_id"),
            "trigger_name": trigger_data.get("trigger_name"),
            "customer_id": trigger_data.get("customer_id"),
            "priority": trigger_data.get("priority"),
            "source": trigger_data.get("source"),
            "conditions_met": trigger_data.get("matched_conditions", []),
            "actions_taken": trigger_data.get("suggested_actions", []),
            "confidence": trigger_data.get("confidence", 0.0),
            "context_summary": self._summarize_context(trigger_data.get("context", {}))
        }
    
    def _summarize_context(self, context: Dict[str, Any]) -> str:
        """Create a summary of trigger context"""
        summary_parts = []
        
        if "matched_keywords" in context:
            keywords = context["matched_keywords"][:3]  # First 3 keywords
            summary_parts.append(f"Keywords: {', '.join(keywords)}")
        
        if "competitor" in context:
            summary_parts.append(f"Competitor: {context['competitor']}")
        
        if "health_score" in context:
            summary_parts.append(f"Health Score: {context['health_score']}")
        
        if "usage_change" in context:
            summary_parts.append(f"Usage Change: {context['usage_change']}%")
        
        return " | ".join(summary_parts)
    
    async def _add_to_daily_report(self, report_entry: Dict[str, Any]):
        """Add entry to daily report"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = self.report_storage_path / f"daily_{today}.json"
        
        await self._append_to_json_file(daily_file, report_entry)
    
    async def _add_to_weekly_report(self, report_entry: Dict[str, Any]):
        """Add entry to weekly report"""
        # Get Monday of current week
        now = datetime.now()
        monday = now - timedelta(days=now.weekday())
        week_start = monday.strftime("%Y-%m-%d")
        
        weekly_file = self.report_storage_path / f"weekly_{week_start}.json"
        
        await self._append_to_json_file(weekly_file, report_entry)
    
    async def _add_to_customer_report(self, report_entry: Dict[str, Any]):
        """Add entry to customer-specific report"""
        customer_id = report_entry.get("customer_id")
        if not customer_id:
            return
        
        customer_file = self.report_storage_path / f"customer_{customer_id}.json"
        
        await self._append_to_json_file(customer_file, report_entry)
    
    async def _append_to_json_file(self, filepath: Path, entry: Dict[str, Any]):
        """Append entry to JSON file"""
        await asyncio.sleep(0.01)  # Simulate file I/O
        
        # In production, properly handle file locking and atomic writes
        print(f"REPORT ENTRY ADDED:")
        print(f"File: {filepath}")
        print(f"Entry: {entry}")


class GenerateReportAction(BaseAction):
    """Generate summary reports from trigger events"""
    
    def __init__(self,
                 action_id: str = "generate_report",
                 name: str = "Generate Report",
                 description: str = "Generate summary reports from trigger data",
                 report_types: List[str] = None,
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.report_types = report_types or ["daily_summary", "customer_health", "trigger_analytics"]
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute report generation"""
        try:
            reports_generated = []
            
            for report_type in self.report_types:
                if await self._should_generate_report(report_type, trigger_data):
                    report_path = await self._generate_report(report_type, trigger_data)
                    reports_generated.append(report_path)
            
            if reports_generated:
                return ActionResult(
                    status=ActionStatus.SUCCESS,
                    message=f"Generated {len(reports_generated)} reports",
                    data={"reports": reports_generated}
                )
            else:
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message="No reports needed at this time"
                )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to generate reports",
                error=str(e)
            )
    
    async def _should_generate_report(self, report_type: str, trigger_data: Dict[str, Any]) -> bool:
        """Determine if report should be generated"""
        # Generate daily summary at end of day
        if report_type == "daily_summary":
            hour = datetime.now().hour
            return hour >= 17  # After 5 PM
        
        # Generate customer health report for health-related triggers
        elif report_type == "customer_health":
            trigger_id = trigger_data.get("trigger_id", "")
            return any(keyword in trigger_id for keyword in ["health", "churn", "usage"])
        
        # Generate trigger analytics for high-priority triggers
        elif report_type == "trigger_analytics":
            priority = trigger_data.get("priority", "medium")
            return priority in ["high", "critical"]
        
        return False
    
    async def _generate_report(self, report_type: str, trigger_data: Dict[str, Any]) -> str:
        """Generate specific report type"""
        await asyncio.sleep(0.1)  # Simulate report generation
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{report_type}_{timestamp}.html"
        
        if report_type == "daily_summary":
            content = await self._generate_daily_summary()
        elif report_type == "customer_health":
            content = await self._generate_customer_health_report(trigger_data)
        elif report_type == "trigger_analytics":
            content = await self._generate_trigger_analytics()
        else:
            content = "Report content not implemented"
        
        print(f"REPORT GENERATED:")
        print(f"Type: {report_type}")
        print(f"Filename: {report_filename}")
        print(f"Content preview: {content[:100]}...")
        
        return report_filename
    
    async def _generate_daily_summary(self) -> str:
        """Generate daily summary report"""
        return """
        <h1>Daily Sales Trigger Summary</h1>
        <p>Date: {date}</p>
        
        <h2>Key Metrics</h2>
        <ul>
            <li>Total Triggers: X</li>
            <li>Critical Alerts: Y</li>
            <li>Customers Affected: Z</li>
        </ul>
        
        <h2>Top Actions Needed</h2>
        <ul>
            <li>Follow up on buying signals: A customers</li>
            <li>Address churn risks: B customers</li>
            <li>Respond to competitive mentions: C customers</li>
        </ul>
        """.format(date=datetime.now().strftime("%Y-%m-%d"))
    
    async def _generate_customer_health_report(self, trigger_data: Dict[str, Any]) -> str:
        """Generate customer health report"""
        customer_id = trigger_data.get("customer_id", "Unknown")
        
        return f"""
        <h1>Customer Health Report: {customer_id}</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        
        <h2>Health Indicators</h2>
        <ul>
            <li>Recent Trigger: {trigger_data.get('trigger_name', 'Unknown')}</li>
            <li>Priority: {trigger_data.get('priority', 'Medium')}</li>
            <li>Risk Level: {self._assess_risk_level(trigger_data)}</li>
        </ul>
        
        <h2>Recommended Actions</h2>
        <ul>
            {''.join(f'<li>{action}</li>' for action in trigger_data.get('suggested_actions', []))}
        </ul>
        """
    
    async def _generate_trigger_analytics(self) -> str:
        """Generate trigger analytics report"""
        return """
        <h1>Trigger Analytics Dashboard</h1>
        
        <h2>Trigger Performance</h2>
        <ul>
            <li>Most Frequent Triggers</li>
            <li>Response Times</li>
            <li>Success Rates</li>
        </ul>
        
        <h2>Customer Insights</h2>
        <ul>
            <li>Customers with Multiple Triggers</li>
            <li>Trigger Patterns by Segment</li>
            <li>Conversion from Triggers</li>
        </ul>
        """
    
    def _assess_risk_level(self, trigger_data: Dict[str, Any]) -> str:
        """Assess customer risk level from trigger data"""
        trigger_id = trigger_data.get("trigger_id", "")
        priority = trigger_data.get("priority", "medium")
        
        if "churn_risk" in trigger_id or priority == "critical":
            return "HIGH"
        elif "usage_drop" in trigger_id or priority == "high":
            return "MEDIUM"
        else:
            return "LOW"