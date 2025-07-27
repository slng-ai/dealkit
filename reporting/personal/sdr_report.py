from .base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class SDRReport(BaseReport):
    """Sales Development Representative Report - Outbound and early engagement"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Engagement Overview
        report += self.format_section(
            "Engagement Summary",
            self._generate_engagement_summary(context)
        )
        
        # Outreach Performance
        report += self.format_section(
            "Outreach Activity",
            self._analyze_outreach_performance(context)
        )
        
        # Response Analysis
        report += self.format_section(
            "Response & Interest Indicators",
            self._analyze_responses(context)
        )
        
        # Contact Coverage
        report += self.format_section(
            "Contact Discovery",
            self._analyze_contact_coverage(context)
        )
        
        # Qualification Status
        report += self.format_section(
            "Qualification Progress",
            self._assess_qualification(context)
        )
        
        # Recommended Actions
        report += self.format_section(
            "Next Outreach Steps",
            self._recommend_outreach_actions(context)
        )
        
        return report
    
    def _generate_engagement_summary(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Current Status\n\n"
        
        # Only show verified data
        stage = customer_data.get('stage', 'Unknown')
        content += self.format_metric("Lead Stage", stage.title())
        
        # Outreach attempts - only if tracked
        outreach_count = customer_data.get('outreach_attempts', 0)
        if outreach_count > 0:
            content += self.format_metric("Outreach Attempts", str(outreach_count))
        else:
            content += self.format_unknown("Outreach Attempts")
        
        # Last interaction - factual
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_ago = (datetime.now() - last_date).days
            content += self.format_metric("Last Contact", f"{days_ago} days ago")
        else:
            content += self.format_unknown("Last Contact")
        
        # Response status
        if 'response_received' in customer_data:
            response_status = "Responded" if customer_data['response_received'] else "No Response"
            content += self.format_metric("Response Status", response_status)
        else:
            content += self.format_unknown("Response Status")
        
        return content
    
    def _analyze_outreach_performance(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        interactions = context.get('interactions', {})
        
        content = "### Outreach Metrics\n\n"
        
        # Email activity - from actual data
        email_data = interactions.get('email', {})
        if email_data:
            total_emails = len(email_data.get('threads', []))
            if total_emails > 0:
                content += self.format_metric("Email Threads", str(total_emails))
            else:
                content += self.format_unknown("Email Activity")
        else:
            content += self.format_unknown("Email Activity")
        
        # Other channels - only if data exists
        slack_data = interactions.get('slack', {})
        if slack_data and slack_data.get('summary', {}).get('total_messages', 0) > 0:
            content += self.format_metric("Slack Messages", str(slack_data['summary']['total_messages']))
        
        # Call attempts - if tracked
        gong_data = interactions.get('gong', {})
        if gong_data and 'calls' in gong_data:
            content += self.format_metric("Call Attempts", str(len(gong_data['calls'])))
        
        content += "\n### Channel Performance\n"
        content += "Data collection in progress for channel-specific metrics.\n"
        
        return content
    
    def _analyze_responses(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Engagement Signals\n\n"
        
        # Only report what we actually know
        positive_signals = []
        negative_signals = []
        
        # Check for actual response data
        if customer_data.get('response_received'):
            positive_signals.append("Email response received")
        
        # Check meeting scheduled
        if customer_data.get('next_meeting'):
            positive_signals.append("Meeting scheduled")
        
        # Check for active Slack engagement
        slack_engagement = context.get('summary', {}).get('slack_activity', {}).get('engagement_level')
        if slack_engagement == 'high':
            positive_signals.append("Active Slack engagement")
        
        # Report findings
        if positive_signals:
            content += "**Positive Indicators:**\n"
            for signal in positive_signals:
                content += f"- ✅ {signal}\n"
        else:
            content += "**Positive Indicators:** None captured yet\n"
        
        # Check for lack of response
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_since = (datetime.now() - last_date).days
            if days_since > 14:
                negative_signals.append(f"No response in {days_since} days")
        
        if negative_signals:
            content += "\n**Areas of Concern:**\n"
            for signal in negative_signals:
                content += f"- ⚠️ {signal}\n"
        
        return content
    
    def _analyze_contact_coverage(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Contact Mapping\n\n"
        
        # Primary contact - only if exists
        primary = customer_data.get('primary_contact', {})
        if primary and primary.get('name'):
            content += "**Primary Contact:**\n"
            content += f"- Name: {primary.get('name')}\n"
            content += f"- Title: {primary.get('title', 'Unknown')}\n"
            content += f"- Email: {primary.get('email', 'Not provided')}\n\n"
        else:
            content += "**Primary Contact:** Not yet identified\n\n"
        
        # Additional contacts
        additional = customer_data.get('additional_contacts', [])
        if additional:
            content += f"**Additional Contacts Identified:** {len(additional)}\n"
            for contact in additional[:3]:  # Show up to 3
                if contact.get('name'):
                    content += f"- {contact.get('name')} ({contact.get('title', 'Role unknown')})\n"
        else:
            content += "**Additional Contacts:** None identified yet\n"
        
        # Suggested actions based on data
        content += "\n### Contact Strategy\n"
        if not primary.get('name'):
            content += self.format_action_required(
                "Identify primary contact",
                "Essential for progressing engagement"
            )
        elif len(additional) < 2:
            content += self.format_action_required(
                "Expand contact network",
                "Multi-threading increases success probability"
            )
        
        return content
    
    def _assess_qualification(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        assessment = customer_data.get('assessment', {})
        
        content = "### BANT Qualification Status\n\n"
        
        # Budget - only show if we have data
        if 'budget_confirmed' in assessment:
            budget_status = "Confirmed" if assessment['budget_confirmed'] else "Not Confirmed"
            content += self.format_metric("Budget", budget_status)
        else:
            content += self.format_unknown("Budget")
        
        # Authority
        if customer_data.get('primary_contact', {}).get('title'):
            content += self.format_metric("Authority", "Contact identified")
        else:
            content += self.format_unknown("Authority")
        
        # Need
        if customer_data.get('use_case'):
            content += self.format_metric("Need", "Use case defined")
        else:
            content += self.format_unknown("Need")
        
        # Timeline
        if customer_data.get('timeline'):
            content += self.format_metric("Timeline", customer_data['timeline'])
        else:
            content += self.format_unknown("Timeline")
        
        # ICP Fit Score - if available
        if 'icp_score' in customer_data:
            content += f"\n**ICP Fit Score:** {customer_data['icp_score']}/10\n"
        
        return content
    
    def _recommend_outreach_actions(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Recommended Next Steps\n\n"
        
        # Base recommendations on actual data
        stage = customer_data.get('stage', 'discovery')
        
        if stage == 'discovery' or stage == 'Unknown':
            # Early stage recommendations
            if not customer_data.get('primary_contact', {}).get('name'):
                content += self.format_action_required(
                    "Research and identify key contacts",
                    "Use LinkedIn and company website to find decision makers"
                )
            
            if customer_data.get('outreach_attempts', 0) == 0:
                content += self.format_action_required(
                    "Send initial outreach",
                    "Personalized email focusing on relevant use case"
                )
            elif customer_data.get('outreach_attempts', 0) < 3:
                content += self.format_action_required(
                    "Follow up with value-add content",
                    "Share case study or industry insight"
                )
            
            if not customer_data.get('response_received'):
                content += self.format_action_required(
                    "Try alternative channel",
                    "Consider LinkedIn message or phone call"
                )
        
        # If engaged but not qualified
        if customer_data.get('response_received') and not assessment.get('budget_confirmed'):
            content += self.format_action_required(
                "Schedule discovery call",
                "Focus on understanding their challenges and budget process"
            )
        
        # Timing recommendation
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_since = (datetime.now() - last_date).days
            
            if days_since > 7:
                content += "\n**Timing:** Immediate action recommended - re-engagement needed\n"
            elif days_since > 3:
                content += "\n**Timing:** Follow up within 24-48 hours\n"
            else:
                content += "\n**Timing:** On track - maintain regular cadence\n"
        
        return content
    
    def _load_customer_data(self, customer_id: str) -> Dict[str, Any]:
        try:
            with open(f'customers/{customer_id}.json', 'r') as f:
                return json.load(f)
        except:
            return {}