"""
Integration between trigger system and reporting
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

# Add reporting modules to path
sys.path.append(str(Path(__file__).parent.parent.parent / "reporting"))

from base_report import BaseReport


class TriggerReportingIntegration:
    """Connects trigger events to the reporting system"""
    
    def __init__(self, trigger_data_path: str = "workspace-setup/reports/trigger_events"):
        self.trigger_data_path = Path(trigger_data_path)
        self.trigger_data_path.mkdir(parents=True, exist_ok=True)
    
    async def add_trigger_to_context(self, customer_id: str, trigger_event: Dict[str, Any]):
        """Add trigger event to customer context for reporting"""
        try:
            # Load existing customer context
            context = await self._load_customer_context(customer_id)
            
            # Add trigger data
            if "trigger_events" not in context:
                context["trigger_events"] = []
            
            context["trigger_events"].append(trigger_event)
            
            # Update summary metrics
            context["summary"] = self._update_summary_with_trigger(
                context.get("summary", {}), 
                trigger_event
            )
            
            # Save updated context
            await self._save_customer_context(customer_id, context)
            
            return True
            
        except Exception as e:
            print(f"Error adding trigger to context: {e}")
            return False
    
    async def _load_customer_context(self, customer_id: str) -> Dict[str, Any]:
        """Load customer context for reporting"""
        context_file = Path(f"customers/profiles/{customer_id}/context_summary.md")
        
        if context_file.exists():
            # In production, parse existing context file
            # For now, return basic structure
            return {
                "customer_id": customer_id,
                "summary": {},
                "trigger_events": []
            }
        else:
            return {
                "customer_id": customer_id,
                "summary": {},
                "trigger_events": []
            }
    
    async def _save_customer_context(self, customer_id: str, context: Dict[str, Any]):
        """Save updated customer context"""
        # In production, update the actual context file
        context_file = self.trigger_data_path / f"customer_{customer_id}_context.json"
        
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2, default=str)
    
    def _update_summary_with_trigger(self, summary: Dict[str, Any], trigger_event: Dict[str, Any]) -> Dict[str, Any]:
        """Update summary metrics with trigger event data"""
        # Initialize trigger tracking
        if "trigger_activity" not in summary:
            summary["trigger_activity"] = {
                "total_triggers": 0,
                "critical_alerts": 0,
                "buying_signals": 0,
                "churn_risks": 0,
                "competitive_mentions": 0,
                "security_inquiries": 0,
                "last_trigger": None
            }
        
        trigger_activity = summary["trigger_activity"]
        
        # Update counts
        trigger_activity["total_triggers"] += 1
        trigger_activity["last_trigger"] = trigger_event.get("timestamp")
        
        # Update specific trigger type counts
        trigger_id = trigger_event.get("trigger_id", "")
        priority = trigger_event.get("priority", "medium")
        
        if priority == "critical":
            trigger_activity["critical_alerts"] += 1
        
        if "buying_signal" in trigger_id:
            trigger_activity["buying_signals"] += 1
        elif "churn_risk" in trigger_id:
            trigger_activity["churn_risks"] += 1
        elif "competitive" in trigger_id:
            trigger_activity["competitive_mentions"] += 1
        elif "security" in trigger_id:
            trigger_activity["security_inquiries"] += 1
        
        # Update engagement score impact
        if "engagement_score" not in summary:
            summary["engagement_score"] = 50  # Default score
        
        # Adjust engagement based on trigger type
        if "buying_signal" in trigger_id:
            summary["engagement_score"] = min(summary["engagement_score"] + 10, 100)
        elif "churn_risk" in trigger_id:
            summary["engagement_score"] = max(summary["engagement_score"] - 20, 0)
        
        return summary
    
    def generate_trigger_summary_for_reports(self, customer_id: str, timeframe_days: int = 30) -> Dict[str, Any]:
        """Generate trigger summary for inclusion in reports"""
        try:
            context_file = self.trigger_data_path / f"customer_{customer_id}_context.json"
            
            if not context_file.exists():
                return self._empty_trigger_summary()
            
            with open(context_file, 'r') as f:
                context = json.load(f)
            
            trigger_events = context.get("trigger_events", [])
            
            # Filter events by timeframe
            cutoff_date = datetime.now() - timedelta(days=timeframe_days)
            recent_events = [
                event for event in trigger_events
                if datetime.fromisoformat(event.get("timestamp", "1970-01-01")) > cutoff_date
            ]
            
            return self._analyze_trigger_events(recent_events)
            
        except Exception as e:
            print(f"Error generating trigger summary: {e}")
            return self._empty_trigger_summary()
    
    def _empty_trigger_summary(self) -> Dict[str, Any]:
        """Return empty trigger summary structure"""
        return {
            "total_triggers": 0,
            "critical_alerts": 0,
            "buying_signals": 0,
            "churn_risks": 0,
            "competitive_mentions": 0,
            "security_inquiries": 0,
            "recent_triggers": [],
            "trigger_trends": "No trigger activity",
            "risk_assessment": "Low",
            "opportunity_signals": []
        }
    
    def _analyze_trigger_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trigger events for reporting insights"""
        if not events:
            return self._empty_trigger_summary()
        
        # Count trigger types
        trigger_counts = {
            "total_triggers": len(events),
            "critical_alerts": 0,
            "buying_signals": 0,
            "churn_risks": 0,
            "competitive_mentions": 0,
            "security_inquiries": 0
        }
        
        recent_triggers = []
        opportunity_signals = []
        risk_indicators = []
        
        for event in events:
            trigger_id = event.get("trigger_id", "")
            priority = event.get("priority", "medium")
            
            # Count by type
            if priority == "critical":
                trigger_counts["critical_alerts"] += 1
            
            if "buying_signal" in trigger_id:
                trigger_counts["buying_signals"] += 1
                opportunity_signals.append(event)
            elif "churn_risk" in trigger_id:
                trigger_counts["churn_risks"] += 1
                risk_indicators.append(event)
            elif "competitive" in trigger_id:
                trigger_counts["competitive_mentions"] += 1
            elif "security" in trigger_id:
                trigger_counts["security_inquiries"] += 1
            
            # Add to recent triggers (last 5)
            if len(recent_triggers) < 5:
                recent_triggers.append({
                    "trigger_name": event.get("trigger_name", "Unknown"),
                    "timestamp": event.get("timestamp"),
                    "priority": priority,
                    "summary": ", ".join(event.get("matched_conditions", [])[:2])
                })
        
        # Assess overall risk
        risk_assessment = self._assess_customer_risk(trigger_counts, risk_indicators)
        
        # Generate trend analysis
        trigger_trends = self._analyze_trigger_trends(events)
        
        return {
            **trigger_counts,
            "recent_triggers": recent_triggers,
            "trigger_trends": trigger_trends,
            "risk_assessment": risk_assessment,
            "opportunity_signals": opportunity_signals[:3],  # Top 3 opportunities
            "risk_indicators": risk_indicators[:3]  # Top 3 risks
        }
    
    def _assess_customer_risk(self, counts: Dict[str, int], risk_events: List[Dict[str, Any]]) -> str:
        """Assess overall customer risk level"""
        # High risk indicators
        if counts["churn_risks"] > 2 or counts["critical_alerts"] > 3:
            return "High"
        
        # Medium risk indicators
        if counts["churn_risks"] > 0 or counts["critical_alerts"] > 1:
            return "Medium"
        
        # Low risk if mostly positive signals
        if counts["buying_signals"] > counts["churn_risks"]:
            return "Low"
        
        return "Medium"
    
    def _analyze_trigger_trends(self, events: List[Dict[str, Any]]) -> str:
        """Analyze trends in trigger activity"""
        if len(events) < 2:
            return "Insufficient data for trend analysis"
        
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda x: x.get("timestamp", ""))
        
        # Compare first half vs second half
        mid_point = len(sorted_events) // 2
        early_events = sorted_events[:mid_point]
        recent_events = sorted_events[mid_point:]
        
        early_risk_events = len([e for e in early_events if "churn_risk" in e.get("trigger_id", "")])
        recent_risk_events = len([e for e in recent_events if "churn_risk" in e.get("trigger_id", "")])
        
        early_opportunity_events = len([e for e in early_events if "buying_signal" in e.get("trigger_id", "")])
        recent_opportunity_events = len([e for e in recent_events if "buying_signal" in e.get("trigger_id", "")])
        
        # Generate trend description
        if recent_risk_events > early_risk_events:
            return "Increasing risk signals - requires attention"
        elif recent_opportunity_events > early_opportunity_events:
            return "Positive momentum - growing buying interest"
        elif len(recent_events) < len(early_events):
            return "Decreasing activity - may need engagement"
        else:
            return "Stable activity levels"


class TriggerAwareReport(BaseReport):
    """Enhanced base report that includes trigger data"""
    
    def __init__(self):
        super().__init__()
        self.trigger_integration = TriggerReportingIntegration()
    
    def generate(self, context: Dict[str, Any]) -> str:
        """Generate report with trigger data included"""
        # Add trigger summary to context
        customer_id = context.get('customer_id', 'unknown')
        trigger_summary = self.trigger_integration.generate_trigger_summary_for_reports(customer_id)
        context['trigger_summary'] = trigger_summary
        
        return self._generate_with_triggers(context)
    
    def _generate_with_triggers(self, context: Dict[str, Any]) -> str:
        """Override in subclasses to include trigger data"""
        return self.generate_original(context)
    
    def generate_original(self, context: Dict[str, Any]) -> str:
        """Original generate method - override in subclasses"""
        return "Base report with no trigger data"
    
    def format_trigger_section(self, context: Dict[str, Any]) -> str:
        """Format trigger activity section for reports"""
        trigger_summary = context.get('trigger_summary', {})
        
        if trigger_summary.get('total_triggers', 0) == 0:
            return self.format_section("Recent Activity", "No automated triggers in the last 30 days.")
        
        content = ""
        
        # Overall metrics
        content += self.format_metric("Total Triggers", trigger_summary.get('total_triggers', 0), "🎯")
        content += self.format_metric("Risk Level", trigger_summary.get('risk_assessment', 'Unknown'), "⚠️")
        content += self.format_metric("Trend", trigger_summary.get('trigger_trends', 'Unknown'), "📈")
        
        # Specific counts
        if trigger_summary.get('buying_signals', 0) > 0:
            content += self.format_metric("Buying Signals", trigger_summary.get('buying_signals', 0), "💰")
        
        if trigger_summary.get('churn_risks', 0) > 0:
            content += self.format_metric("Churn Risks", trigger_summary.get('churn_risks', 0), "🚨")
        
        if trigger_summary.get('competitive_mentions', 0) > 0:
            content += self.format_metric("Competitive Mentions", trigger_summary.get('competitive_mentions', 0), "⚔️")
        
        # Recent triggers
        recent_triggers = trigger_summary.get('recent_triggers', [])
        if recent_triggers:
            content += "\n**Recent Trigger Events:**\n"
            for trigger in recent_triggers[:3]:
                timestamp = trigger.get('timestamp', '')[:10]  # Just date
                content += f"- {timestamp}: {trigger.get('trigger_name', 'Unknown')} ({trigger.get('priority', 'medium')})\n"
        
        return self.format_section("Trigger Activity (30 days)", content)
    
    def format_risk_opportunities_section(self, context: Dict[str, Any]) -> str:
        """Format risks and opportunities section"""
        trigger_summary = context.get('trigger_summary', {})
        
        content = ""
        
        # Opportunities
        opportunities = trigger_summary.get('opportunity_signals', [])
        if opportunities:
            content += "**Opportunities:**\n"
            for opp in opportunities:
                conditions = ", ".join(opp.get('matched_conditions', [])[:2])
                content += f"- {conditions}\n"
            content += "\n"
        
        # Risks
        risks = trigger_summary.get('risk_indicators', [])
        if risks:
            content += "**Risk Indicators:**\n"
            for risk in risks:
                conditions = ", ".join(risk.get('matched_conditions', [])[:2])
                content += f"- {conditions}\n"
            content += "\n"
        
        # Suggested actions
        risk_level = trigger_summary.get('risk_assessment', 'Low')
        if risk_level == "High":
            content += self.format_action_required(
                "Schedule immediate retention call",
                "High churn risk detected from recent activity"
            )
        elif opportunities:
            content += self.format_action_required(
                "Follow up on buying signals",
                "Customer showing purchase intent"
            )
        
        if content:
            return self.format_section("Risks & Opportunities", content)
        else:
            return ""


# Example enhanced report class
class TriggerAwareCROReport(TriggerAwareReport):
    """CRO report enhanced with trigger data"""
    
    def _generate_with_triggers(self, context: Dict[str, Any]) -> str:
        """Generate CRO report with trigger insights"""
        report = self.format_header(context)
        
        # Executive summary with trigger insights
        trigger_summary = context.get('trigger_summary', {})
        
        exec_summary = "## Executive Summary\n\n"
        
        # Key metrics
        engagement_score = self.calculate_engagement_score(context)
        exec_summary += self.format_metric("Engagement Score", f"{engagement_score}/100", "📊")
        exec_summary += self.format_metric("Risk Level", trigger_summary.get('risk_assessment', 'Unknown'), "⚠️")
        exec_summary += self.format_metric("Opportunity Signals", trigger_summary.get('buying_signals', 0), "💰")
        
        # Strategic insights
        if trigger_summary.get('risk_assessment') == "High":
            exec_summary += "\n🚨 **URGENT:** High churn risk detected. Immediate intervention required.\n"
        elif trigger_summary.get('buying_signals', 0) > 2:
            exec_summary += "\n🎯 **OPPORTUNITY:** Strong buying signals detected. Consider acceleration.\n"
        
        report += exec_summary + "\n"
        
        # Include trigger activity section
        report += self.format_trigger_section(context)
        
        # Include risks and opportunities
        report += self.format_risk_opportunities_section(context)
        
        return report