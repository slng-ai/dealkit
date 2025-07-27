from ..base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class DealAlert(BaseReport):
    """Deal Alert Report - Real-time notifications for deal status changes and opportunities"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        alert_type = context.get('alert_type', 'all')
        
        if alert_type == 'critical':
            return self._generate_critical_alerts(context)
        elif alert_type == 'opportunity':
            return self._generate_opportunity_alerts(context)
        elif alert_type == 'risk':
            return self._generate_risk_alerts(context)
        else:
            return self._generate_all_alerts(context)
    
    def _generate_all_alerts(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Critical Alerts (Immediate Action)
        report += self.format_section(
            "🔴 CRITICAL ALERTS - Immediate Action Required",
            self._generate_critical_alerts(context)
        )
        
        # Opportunity Alerts  
        report += self.format_section(
            "🟢 OPPORTUNITY ALERTS - Act Within 24 Hours",
            self._generate_opportunity_alerts(context)
        )
        
        # Risk Alerts
        report += self.format_section(
            "🟡 RISK ALERTS - Monitor Closely",
            self._generate_risk_alerts(context)
        )
        
        # Performance Pulse
        report += self.format_section(
            "📊 PERFORMANCE PULSE",
            self._generate_performance_pulse(context)
        )
        
        return report
    
    def _generate_critical_alerts(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = ""
        critical_alerts = []
        
        # Deal stalled alert
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_since = (datetime.now() - last_date).days
            
            if days_since > 14:
                critical_alerts.append({
                    'type': 'DEAL STALLED',
                    'urgency': 'IMMEDIATE',
                    'message': f"No activity in {days_since} days",
                    'action': 'Contact customer immediately',
                    'owner': customer_data.get('primary_contact', {}).get('name', 'Unknown'),
                    'deal_value': customer_data.get('deal_size', 0)
                })
        
        # Contract expiration alert
        contract_end = customer_data.get('contract_end_date')
        if contract_end:
            end_date = datetime.fromisoformat(contract_end)
            days_to_expiry = (end_date - datetime.now()).days
            
            if 0 <= days_to_expiry <= 30:
                critical_alerts.append({
                    'type': 'CONTRACT EXPIRING',
                    'urgency': 'CRITICAL',
                    'message': f"Contract expires in {days_to_expiry} days",
                    'action': 'Initiate renewal discussion',
                    'owner': 'Customer Success Manager',
                    'deal_value': customer_data.get('deal_size', 0)
                })
        
        # Budget deadline alert
        budget_deadline = customer_data.get('budget_deadline')
        if budget_deadline:
            deadline_date = datetime.fromisoformat(budget_deadline)
            days_to_deadline = (deadline_date - datetime.now()).days
            
            if 0 <= days_to_deadline <= 7:
                critical_alerts.append({
                    'type': 'BUDGET DEADLINE',
                    'urgency': 'CRITICAL',
                    'message': f"Budget deadline in {days_to_deadline} days",
                    'action': 'Accelerate closing process',
                    'owner': customer_data.get('account_owner', 'Account Executive'),
                    'deal_value': customer_data.get('deal_size', 0)
                })
        
        # Competitive threat alert
        if customer_data.get('assessment', {}).get('competition'):
            competitive_mentions = context.get('recent_competitive_mentions', 0)
            if competitive_mentions > 0:
                critical_alerts.append({
                    'type': 'COMPETITIVE THREAT',
                    'urgency': 'HIGH',
                    'message': f"{competitive_mentions} recent competitive mentions",
                    'action': 'Deploy competitive battlecard',
                    'owner': customer_data.get('account_owner', 'Account Executive'),
                    'deal_value': customer_data.get('deal_size', 0)
                })
        
        # Customer health score drop
        health_score = customer_data.get('health_score', 100)
        if health_score < 40:
            critical_alerts.append({
                'type': 'HEALTH SCORE DROP',
                'urgency': 'CRITICAL',
                'message': f"Customer health score: {health_score}/100",
                'action': 'Customer success intervention required',
                'owner': 'Customer Success Manager',
                'deal_value': customer_data.get('deal_size', 0)
            })
        
        # Format critical alerts
        if critical_alerts:
            # Sort by deal value (highest first)
            critical_alerts.sort(key=lambda x: x['deal_value'], reverse=True)
            
            for alert in critical_alerts:
                urgency_emoji = {"IMMEDIATE": "🚨", "CRITICAL": "🔴", "HIGH": "⚠️"}.get(alert['urgency'], "❗")
                content += f"### {urgency_emoji} {alert['type']}\n"
                content += f"**Customer:** {customer_data.get('company_name', 'Unknown')}\n"
                content += f"**Deal Value:** {self._format_currency(alert['deal_value'])}\n"
                content += f"**Alert:** {alert['message']}\n"
                content += f"**Required Action:** {alert['action']}\n"
                content += f"**Owner:** {alert['owner']}\n"
                content += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        else:
            content = "✅ No critical alerts at this time\n"
        
        return content
    
    def _generate_opportunity_alerts(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = ""
        opportunity_alerts = []
        
        # Buying signal detected
        buying_signals = context.get('buying_signals', [])
        if buying_signals:
            for signal in buying_signals:
                opportunity_alerts.append({
                    'type': 'BUYING SIGNAL',
                    'priority': 'HIGH',
                    'message': f"Detected: {signal['signal']}",
                    'action': 'Follow up within 4 hours',
                    'source': signal.get('source', 'Email'),
                    'confidence': signal.get('confidence', 'Medium')
                })
        
        # New stakeholder identified
        new_stakeholders = context.get('new_stakeholders', [])
        for stakeholder in new_stakeholders:
            opportunity_alerts.append({
                'type': 'NEW STAKEHOLDER',
                'priority': 'MEDIUM',
                'message': f"New contact: {stakeholder.get('name', 'Unknown')} ({stakeholder.get('title', 'Unknown')})",
                'action': 'Reach out for introduction',
                'source': 'Relationship mapping',
                'confidence': 'High'
            })
        
        # Usage spike detected
        usage_increase = context.get('usage_increase_percentage', 0)
        if usage_increase > 50:
            opportunity_alerts.append({
                'type': 'USAGE SPIKE',
                'priority': 'HIGH',
                'message': f"Platform usage increased {usage_increase}% this week",
                'action': 'Explore expansion opportunity',
                'source': 'Product analytics',
                'confidence': 'High'
            })
        
        # Demo request
        if context.get('demo_requested'):
            opportunity_alerts.append({
                'type': 'DEMO REQUEST',
                'priority': 'HIGH',
                'message': "Customer requested product demonstration",
                'action': 'Schedule demo within 24 hours',
                'source': 'Inbound request',
                'confidence': 'High'
            })
        
        # Reference mention
        if context.get('reference_mention'):
            opportunity_alerts.append({
                'type': 'REFERENCE OPPORTUNITY',
                'priority': 'MEDIUM',
                'message': "Customer expressed willingness to be reference",
                'action': 'Coordinate reference call setup',
                'source': 'Customer conversation',
                'confidence': 'Medium'
            })
        
        # Format opportunity alerts
        if opportunity_alerts:
            for alert in opportunity_alerts:
                priority_emoji = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "⚪"}.get(alert['priority'], "📝")
                content += f"### {priority_emoji} {alert['type']}\n"
                content += f"**Customer:** {customer_data.get('company_name', 'Unknown')}\n"
                content += f"**Opportunity:** {alert['message']}\n"
                content += f"**Action:** {alert['action']}\n"
                content += f"**Source:** {alert['source']}\n"
                content += f"**Confidence:** {alert['confidence']}\n"
                content += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        else:
            content = "📭 No new opportunities detected\n"
        
        return content
    
    def _generate_risk_alerts(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = ""
        risk_alerts = []
        
        # Single-threaded deal risk
        additional_contacts = len(customer_data.get('additional_contacts', []))
        if additional_contacts < 2:
            risk_alerts.append({
                'type': 'SINGLE-THREADED',
                'risk_level': 'HIGH',
                'message': f"Only {additional_contacts + 1} contact(s) identified",
                'impact': 'Deal could stall if champion leaves',
                'mitigation': 'Identify and engage 2-3 additional stakeholders'
            })
        
        # Budget not confirmed risk
        if not customer_data.get('assessment', {}).get('budget_confirmed'):
            risk_alerts.append({
                'type': 'UNCONFIRMED BUDGET',
                'risk_level': 'MEDIUM',
                'message': "Budget approval process unclear",
                'impact': 'Deal could be delayed or reduced',
                'mitigation': 'Get written budget confirmation from economic buyer'
            })
        
        # Support ticket spike
        support_tickets = context.get('support_tickets_last_week', 0)
        if support_tickets > 5:
            risk_alerts.append({
                'type': 'SUPPORT SPIKE',
                'risk_level': 'MEDIUM',
                'message': f"{support_tickets} support tickets this week",
                'impact': 'Customer satisfaction may be declining',
                'mitigation': 'Customer success manager intervention'
            })
        
        # Non-response to outreach
        days_since_response = context.get('days_since_last_response', 0)
        if days_since_response > 7:
            risk_alerts.append({
                'type': 'NON-RESPONSIVE',
                'risk_level': 'MEDIUM',
                'message': f"No response to outreach in {days_since_response} days",
                'impact': 'Loss of engagement and momentum',
                'mitigation': 'Try alternative communication channel'
            })
        
        # Competitor evaluation
        if customer_data.get('assessment', {}).get('evaluating_competitors'):
            risk_alerts.append({
                'type': 'COMPETITIVE EVALUATION',
                'risk_level': 'HIGH',
                'message': "Customer actively evaluating competitors",
                'impact': 'Risk of losing deal to competition',
                'mitigation': 'Emphasize unique value propositions and ROI'
            })
        
        # Format risk alerts
        if risk_alerts:
            for alert in risk_alerts:
                risk_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(alert['risk_level'], "⚠️")
                content += f"### {risk_emoji} {alert['type']}\n"
                content += f"**Customer:** {customer_data.get('company_name', 'Unknown')}\n"
                content += f"**Risk:** {alert['message']}\n"
                content += f"**Potential Impact:** {alert['impact']}\n"
                content += f"**Recommended Mitigation:** {alert['mitigation']}\n"
                content += f"**Risk Level:** {alert['risk_level']}\n"
                content += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        else:
            content = "✅ No significant risks detected\n"
        
        return content
    
    def _generate_performance_pulse(self, context: Dict[str, Any]) -> str:
        content = "### Real-Time Performance Indicators\n\n"
        
        # Daily activity pulse
        daily_metrics = context.get('daily_metrics', {})
        content += "**Today's Activity:**\n"
        content += self.format_metric("Calls Made", str(daily_metrics.get('calls', 0)))
        content += self.format_metric("Emails Sent", str(daily_metrics.get('emails', 0)))
        content += self.format_metric("Meetings Held", str(daily_metrics.get('meetings', 0)))
        content += self.format_metric("Demos Delivered", str(daily_metrics.get('demos', 0)))
        
        # Pipeline movement
        content += "\n**Pipeline Activity (Last 24 Hours):**\n"
        pipeline_activity = context.get('pipeline_activity', {})
        content += self.format_metric("New Opportunities", str(pipeline_activity.get('new_opps', 0)))
        content += self.format_metric("Stage Progressions", str(pipeline_activity.get('progressions', 0)))
        content += self.format_metric("Deals Closed", str(pipeline_activity.get('closed', 0)))
        
        # Goal tracking
        content += "\n**Goal Progress:**\n"
        goals = context.get('daily_goals', {})
        actuals = context.get('daily_actuals', {})
        
        for goal_type, target in goals.items():
            actual = actuals.get(goal_type, 0)
            percentage = (actual / target) * 100 if target > 0 else 0
            status = "✅" if percentage >= 100 else "🟡" if percentage >= 75 else "🔴"
            content += f"- {goal_type.title()}: {actual}/{target} ({percentage:.0f}%) {status}\n"
        
        # Trending alerts
        content += "\n**Trending This Week:**\n"
        trends = context.get('trending_alerts', [])
        if trends:
            for trend in trends:
                content += f"- {trend}\n"
        else:
            content += "- No significant trends detected\n"
        
        return content
    
    def _load_customer_data(self, customer_id: str) -> Dict[str, Any]:
        try:
            with open(f'customers/{customer_id}.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _format_currency(self, amount: float) -> str:
        if amount >= 1000000:
            return f"${amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"${amount/1000:.0f}K"
        else:
            return f"${amount:.0f}"