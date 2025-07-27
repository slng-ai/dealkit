from ..base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class AEReport(BaseReport):
    """Account Executive Report - Individual deal management and activity tracking"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Daily Activities Overview
        report += self.format_section(
            "Today's Activities",
            self._generate_activity_summary(context)
        )
        
        # Deal Pipeline Status
        report += self.format_section(
            "Active Deals Status",
            self._analyze_deal_pipeline(context)
        )
        
        # Goal Progress
        report += self.format_section(
            "Goal Progress",
            self._track_goal_progress(context)
        )
        
        # Priority Actions
        report += self.format_section(
            "Priority Actions",
            self._identify_priority_actions(context)
        )
        
        # Tomorrow's Focus
        report += self.format_section(
            "Tomorrow's Focus",
            self._plan_tomorrow_focus(context)
        )
        
        return report
    
    def _generate_activity_summary(self, context: Dict[str, Any]) -> str:
        user_id = context.get('user_id', '')
        
        content = "### Today's Performance\n\n"
        
        # Activity metrics
        activities = context.get('daily_activities', {})
        content += "**Activities Completed:**\n"
        content += self.format_metric("Calls Made", str(activities.get('calls', 0)))
        content += self.format_metric("Emails Sent", str(activities.get('emails', 0)))
        content += self.format_metric("Demos Delivered", str(activities.get('demos', 0)))
        content += self.format_metric("Meetings Held", str(activities.get('meetings', 0)))
        
        # Daily goals vs actuals
        goals = context.get('daily_goals', {})
        content += "\n**Goal Achievement:**\n"
        for activity, actual in activities.items():
            goal = goals.get(activity, 0)
            if goal > 0:
                percentage = (actual / goal) * 100
                status = "✅" if percentage >= 100 else "🟡" if percentage >= 75 else "🔴"
                content += f"- {activity.title()}: {actual}/{goal} ({percentage:.0f}%) {status}\n"
        
        # Time utilization
        content += "\n**Time Allocation:**\n"
        content += "- Prospecting: 25% (2 hours)\n"
        content += "- Customer Meetings: 40% (3.2 hours)\n"
        content += "- Administrative: 20% (1.6 hours)\n"
        content += "- Follow-up: 15% (1.2 hours)\n"
        
        return content
    
    def _analyze_deal_pipeline(self, context: Dict[str, Any]) -> str:
        user_id = context.get('user_id', '')
        
        content = "### Active Opportunities\n\n"
        
        # Pipeline summary
        pipeline = context.get('pipeline', {})
        total_value = sum(deal.get('value', 0) for deal in pipeline.get('deals', []))
        
        content += self.format_metric("Total Pipeline Value", self._format_currency(total_value))
        content += self.format_metric("Number of Active Deals", str(len(pipeline.get('deals', []))))
        content += self.format_metric("Average Deal Size", self._format_currency(total_value / max(1, len(pipeline.get('deals', [])))))
        
        # Deals by stage
        content += "\n**Pipeline by Stage:**\n"
        stage_summary = {}
        for deal in pipeline.get('deals', []):
            stage = deal.get('stage', 'unknown')
            if stage not in stage_summary:
                stage_summary[stage] = {'count': 0, 'value': 0}
            stage_summary[stage]['count'] += 1
            stage_summary[stage]['value'] += deal.get('value', 0)
        
        for stage, data in stage_summary.items():
            content += f"- {stage.title()}: {data['count']} deals ({self._format_currency(data['value'])})\n"
        
        # Deals requiring attention
        content += "\n**Immediate Attention Required:**\n"
        urgent_deals = [d for d in pipeline.get('deals', []) if self._is_deal_urgent(d)]
        
        if urgent_deals:
            for deal in urgent_deals[:3]:  # Top 3 urgent
                content += f"- **{deal.get('company', 'Unknown')}**: {deal.get('urgency_reason', 'No recent activity')}\n"
        else:
            content += "- ✅ All deals have recent activity\n"
        
        return content
    
    def _track_goal_progress(self, context: Dict[str, Any]) -> str:
        content = "### Weekly & Monthly Progress\n\n"
        
        # Weekly progress
        weekly_progress = context.get('weekly_progress', {})
        content += "**This Week's Progress:**\n"
        content += self.format_metric("Revenue Closed", self._format_currency(weekly_progress.get('revenue_closed', 0)))
        content += self.format_metric("New Opportunities", str(weekly_progress.get('new_opps', 0)))
        content += self.format_metric("Demos Completed", str(weekly_progress.get('demos', 0)))
        content += self.format_metric("Proposals Sent", str(weekly_progress.get('proposals', 0)))
        
        # Monthly quota progress
        monthly_progress = context.get('monthly_progress', {})
        quota = monthly_progress.get('quota', 100000)
        achieved = monthly_progress.get('achieved', 0)
        percentage = (achieved / quota) * 100 if quota > 0 else 0
        
        content += "\n**Monthly Quota Progress:**\n"
        content += self.format_metric("Quota Target", self._format_currency(quota))
        content += self.format_metric("Revenue Achieved", self._format_currency(achieved))
        content += self.format_metric("Quota Attainment", f"{percentage:.1f}%")
        
        # Days remaining
        today = datetime.now()
        end_of_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
        days_remaining = (end_of_month - today).days
        
        if days_remaining > 0:
            daily_target = (quota - achieved) / days_remaining
            content += self.format_metric("Days Remaining", str(days_remaining))
            content += self.format_metric("Daily Target Needed", self._format_currency(daily_target))
        
        return content
    
    def _identify_priority_actions(self, context: Dict[str, Any]) -> str:
        content = "### Today's Priorities\n\n"
        
        # Generate priority actions based on pipeline and activities
        actions = []
        
        # Check for overdue follow-ups
        pipeline = context.get('pipeline', {})
        for deal in pipeline.get('deals', []):
            last_activity = deal.get('last_activity')
            if last_activity:
                last_date = datetime.fromisoformat(last_activity)
                days_since = (datetime.now() - last_date).days
                if days_since > 7:
                    actions.append({
                        'priority': 'high',
                        'action': f"Follow up with {deal.get('company', 'Unknown')}",
                        'reason': f"No activity in {days_since} days",
                        'estimated_time': '30 minutes'
                    })
        
        # Check for upcoming meetings
        upcoming_meetings = context.get('upcoming_meetings', [])
        for meeting in upcoming_meetings:
            if meeting.get('preparation_needed'):
                actions.append({
                    'priority': 'medium',
                    'action': f"Prepare for {meeting.get('title', 'meeting')}",
                    'reason': f"Meeting with {meeting.get('attendees', 'stakeholders')} scheduled",
                    'estimated_time': '45 minutes'
                })
        
        # Check for proposals to send
        pending_proposals = context.get('pending_proposals', [])
        for proposal in pending_proposals:
            actions.append({
                'priority': 'high',
                'action': f"Send proposal to {proposal.get('company', 'prospect')}",
                'reason': "Proposal requested and ready for delivery",
                'estimated_time': '20 minutes'
            })
        
        # Sort by priority and format
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        actions.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        for i, action in enumerate(actions[:5], 1):  # Top 5 actions
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(action['priority'], "⚫")
            content += f"**{i}. {priority_emoji} {action['action']}**\n"
            content += f"   - Why: {action['reason']}\n"
            content += f"   - Time: {action['estimated_time']}\n\n"
        
        if not actions:
            content += "✅ No urgent actions identified - great job staying on top of your pipeline!\n"
        
        return content
    
    def _plan_tomorrow_focus(self, context: Dict[str, Any]) -> str:
        content = "### Tomorrow's Focus Areas\n\n"
        
        # Scheduled meetings
        tomorrow_meetings = context.get('tomorrow_meetings', [])
        if tomorrow_meetings:
            content += "**Scheduled Meetings:**\n"
            for meeting in tomorrow_meetings:
                time = meeting.get('time', 'TBD')
                title = meeting.get('title', 'Meeting')
                content += f"- {time}: {title}\n"
        else:
            content += "**Meetings:** None scheduled - opportunity for prospecting focus\n"
        
        content += "\n**Recommended Focus:**\n"
        
        # Based on current pipeline needs
        weekly_progress = context.get('weekly_progress', {})
        
        if weekly_progress.get('new_opps', 0) < 3:
            content += "- 🎯 **Prospecting Priority**: Add 2-3 new opportunities to pipeline\n"
        
        if weekly_progress.get('demos', 0) < 2:
            content += "- 🎯 **Demo Focus**: Schedule and deliver product demonstrations\n"
        
        if weekly_progress.get('proposals', 0) == 0:
            content += "- 🎯 **Proposal Development**: Advance qualified opportunities to proposal stage\n"
        
        # Time blocking suggestions
        content += "\n**Suggested Time Blocks:**\n"
        content += "- 9:00-11:00 AM: Prospecting and outbound activities\n"
        content += "- 11:00-12:00 PM: Follow-up calls and emails\n"
        content += "- 1:00-3:00 PM: Customer meetings and demos\n"
        content += "- 3:00-4:00 PM: Proposal development and admin\n"
        content += "- 4:00-5:00 PM: Pipeline review and planning\n"
        
        return content
    
    def _is_deal_urgent(self, deal: Dict[str, Any]) -> bool:
        """Determine if a deal requires urgent attention"""
        last_activity = deal.get('last_activity')
        if last_activity:
            last_date = datetime.fromisoformat(last_activity)
            days_since = (datetime.now() - last_date).days
            return days_since > 7
        return True
    
    def _format_currency(self, amount: float) -> str:
        if amount >= 1000000:
            return f"${amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"${amount/1000:.0f}K"
        else:
            return f"${amount:.0f}"