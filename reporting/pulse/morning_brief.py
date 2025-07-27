from ..base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class MorningBrief(BaseReport):
    """Morning Brief Report - Daily priorities and immediate actions"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Today's Schedule
        report += self.format_section(
            "📅 Today's Schedule",
            self._generate_schedule_summary(context)
        )
        
        # Urgent Actions
        report += self.format_section(
            "🚨 Urgent Actions Required",
            self._identify_urgent_actions(context)
        )
        
        # Pipeline Priorities
        report += self.format_section(
            "🎯 Pipeline Priorities",
            self._identify_pipeline_priorities(context)
        )
        
        # Goal Progress
        report += self.format_section(
            "📊 Daily Goal Tracking",
            self._track_daily_goals(context)
        )
        
        # Key Reminders
        report += self.format_section(
            "💡 Key Reminders",
            self._generate_reminders(context)
        )
        
        return report
    
    def _generate_schedule_summary(self, context: Dict[str, Any]) -> str:
        content = ""
        
        today_meetings = context.get('today_meetings', [])
        if today_meetings:
            content += "**Scheduled Meetings:**\n"
            for meeting in today_meetings:
                time = meeting.get('time', 'TBD')
                title = meeting.get('title', 'Meeting')
                attendees = meeting.get('attendees', 'Unknown')
                preparation = "🔴 Needs prep" if meeting.get('needs_preparation') else "✅ Ready"
                
                content += f"- **{time}**: {title}\n"
                content += f"  - Attendees: {attendees}\n"
                content += f"  - Status: {preparation}\n\n"
        else:
            content += "**No meetings scheduled** - Great day for prospecting and pipeline development!\n\n"
        
        # Travel requirements
        travel = context.get('travel_today', {})
        if travel.get('required'):
            content += f"**Travel Required:** {travel.get('destination', 'Unknown')} at {travel.get('departure_time', 'TBD')}\n"
        
        # Available time blocks
        available_hours = context.get('available_hours', 6)
        content += f"**Available Time for Sales Activities:** {available_hours} hours\n"
        
        return content
    
    def _identify_urgent_actions(self, context: Dict[str, Any]) -> str:
        content = ""
        urgent_actions = []
        
        # Overdue follow-ups
        overdue_followups = context.get('overdue_followups', [])
        for followup in overdue_followups:
            days_overdue = followup.get('days_overdue', 0)
            urgent_actions.append({
                'action': f"Follow up with {followup.get('company', 'prospect')}",
                'reason': f"Overdue by {days_overdue} days",
                'priority': 'critical' if days_overdue > 14 else 'high',
                'time_needed': '15 minutes'
            })
        
        # Expiring opportunities
        expiring_opps = context.get('expiring_opportunities', [])
        for opp in expiring_opps:
            urgent_actions.append({
                'action': f"Contact {opp.get('company', 'prospect')} immediately",
                'reason': f"Budget deadline in {opp.get('days_to_deadline', 0)} days",
                'priority': 'critical',
                'time_needed': '30 minutes'
            })
        
        # Competitive threats
        competitive_threats = context.get('competitive_threats', [])
        for threat in competitive_threats:
            urgent_actions.append({
                'action': f"Address competitive situation at {threat.get('company', 'prospect')}",
                'reason': f"Competitor {threat.get('competitor', 'unknown')} mentioned",
                'priority': 'high',
                'time_needed': '45 minutes'
            })
        
        # Customer health alerts
        health_alerts = context.get('customer_health_alerts', [])
        for alert in health_alerts:
            urgent_actions.append({
                'action': f"Customer success intervention for {alert.get('company', 'customer')}",
                'reason': f"Health score dropped to {alert.get('health_score', 0)}/100",
                'priority': 'high',
                'time_needed': '30 minutes'
            })
        
        if urgent_actions:
            # Sort by priority
            priority_order = {'critical': 1, 'high': 2, 'medium': 3}
            urgent_actions.sort(key=lambda x: priority_order.get(x['priority'], 4))
            
            for i, action in enumerate(urgent_actions[:5], 1):
                priority_emoji = {'critical': '🔴', 'high': '🟡', 'medium': '🟠'}.get(action['priority'], '⚫')
                content += f"**{i}. {priority_emoji} {action['action']}**\n"
                content += f"   - Reason: {action['reason']}\n"
                content += f"   - Time needed: {action['time_needed']}\n\n"
        else:
            content = "✅ No urgent actions identified - you're caught up!\n"
        
        return content
    
    def _identify_pipeline_priorities(self, context: Dict[str, Any]) -> str:
        content = ""
        
        # Deals requiring attention
        priority_deals = context.get('priority_deals', [])
        if priority_deals:
            content += "**High-Priority Deals:**\n"
            for deal in priority_deals[:3]:
                company = deal.get('company', 'Unknown')
                value = deal.get('value', 0)
                stage = deal.get('stage', 'unknown')
                next_action = deal.get('next_action', 'Follow up')
                
                content += f"- **{company}** ({self._format_currency(value)})\n"
                content += f"  - Stage: {stage.title()}\n"
                content += f"  - Next Action: {next_action}\n\n"
        
        # Pipeline building goals
        new_opp_goal = context.get('daily_new_opp_goal', 2)
        current_new_opps = context.get('current_new_opps', 0)
        remaining_opps = max(0, new_opp_goal - current_new_opps)
        
        if remaining_opps > 0:
            content += f"**Pipeline Building Goal:** {remaining_opps} new opportunities needed today\n"
            content += "- Focus on high-value prospects\n"
            content += "- Prioritize inbound leads\n"
            content += "- Follow up on demo requests\n\n"
        else:
            content += "✅ Daily pipeline building goal achieved!\n\n"
        
        # Demo and meeting targets
        demo_goal = context.get('daily_demo_goal', 1)
        current_demos = context.get('current_demos', 0)
        
        if current_demos < demo_goal:
            content += f"**Demo Goal:** Schedule {demo_goal - current_demos} more demo(s) today\n"
        
        return content
    
    def _track_daily_goals(self, context: Dict[str, Any]) -> str:
        content = ""
        
        daily_goals = context.get('daily_goals', {})
        current_progress = context.get('current_progress', {})
        
        content += "**Today's Activity Goals:**\n"
        
        for goal_type, target in daily_goals.items():
            current = current_progress.get(goal_type, 0)
            remaining = max(0, target - current)
            percentage = (current / target * 100) if target > 0 else 0
            
            if percentage >= 100:
                status = "✅ Complete"
            elif percentage >= 75:
                status = "🟡 On track"
            elif percentage >= 50:
                status = "🟠 Needs focus"
            else:
                status = "🔴 Behind"
            
            content += f"- {goal_type.title()}: {current}/{target} ({percentage:.0f}%) {status}\n"
            
            if remaining > 0:
                content += f"  - {remaining} more needed\n"
        
        # Weekly progress context
        weekly_progress = context.get('weekly_progress', {})
        content += "\n**Weekly Context:**\n"
        content += f"- Revenue closed: {self._format_currency(weekly_progress.get('revenue', 0))}\n"
        content += f"- New opportunities: {weekly_progress.get('new_opps', 0)}\n"
        content += f"- Demos completed: {weekly_progress.get('demos', 0)}\n"
        
        return content
    
    def _generate_reminders(self, context: Dict[str, Any]) -> str:
        content = ""
        
        reminders = []
        
        # Follow-up reminders
        followups_due = context.get('followups_due_today', [])
        for followup in followups_due:
            reminders.append(f"Follow up with {followup.get('company', 'prospect')} - promised response today")
        
        # Proposal deadlines
        proposals_due = context.get('proposals_due', [])
        for proposal in proposals_due:
            reminders.append(f"Send proposal to {proposal.get('company', 'prospect')} - due today")
        
        # Contract renewals
        renewals_approaching = context.get('renewals_approaching', [])
        for renewal in renewals_approaching:
            days_to_renewal = renewal.get('days_to_renewal', 0)
            if days_to_renewal <= 30:
                reminders.append(f"Start renewal discussion with {renewal.get('company', 'customer')} - {days_to_renewal} days until expiry")
        
        # Important dates
        important_dates = context.get('important_dates', [])
        for date_info in important_dates:
            reminders.append(f"{date_info.get('event', 'Event')} - {date_info.get('description', 'No details')}")
        
        # CRM hygiene
        outdated_opps = context.get('outdated_opportunities', 0)
        if outdated_opps > 0:
            reminders.append(f"Update {outdated_opps} opportunities in CRM - stale data affects forecasting")
        
        if reminders:
            for reminder in reminders[:5]:
                content += f"• {reminder}\n"
        else:
            content = "• No special reminders today - focus on your core activities!\n"
        
        # Daily affirmation/tip
        tips = [
            "Remember: Every 'no' gets you closer to a 'yes'",
            "Focus on value in every customer interaction",
            "Ask great questions to uncover real business needs",
            "Your pipeline is your paycheck - keep it full",
            "Consistency in activities leads to consistent results"
        ]
        
        import random
        daily_tip = random.choice(tips)
        content += f"\n💡 **Daily Tip:** {daily_tip}\n"
        
        return content
    
    def _format_currency(self, amount: float) -> str:
        if amount >= 1000000:
            return f"${amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"${amount/1000:.0f}K"
        else:
            return f"${amount:.0f}"