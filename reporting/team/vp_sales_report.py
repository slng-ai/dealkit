from ..base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class VPSalesReport(BaseReport):
    """VP Sales Report - Team performance, pipeline health, and strategic metrics"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Team Performance Overview
        report += self.format_section(
            "Team Performance Dashboard",
            self._generate_team_performance(context)
        )
        
        # Pipeline Health Analysis
        report += self.format_section(
            "Pipeline Health & Velocity",
            self._analyze_pipeline_health(context)
        )
        
        # Quota Attainment Tracking
        report += self.format_section(
            "Quota Attainment Analysis",
            self._track_quota_performance(context)
        )
        
        # Sales Efficiency Metrics
        report += self.format_section(
            "Sales Efficiency & Productivity",
            self._analyze_sales_efficiency(context)
        )
        
        # Competitive Intelligence
        report += self.format_section(
            "Competitive Landscape",
            self._analyze_competitive_position(context)
        )
        
        # Strategic Recommendations
        report += self.format_section(
            "Strategic Actions",
            self._generate_strategic_actions(context)
        )
        
        return report
    
    def _generate_team_performance(self, context: Dict[str, Any]) -> str:
        team_data = context.get('team_data', {})
        
        content = "### Team Overview\n\n"
        
        # Team size and composition
        team_size = len(team_data.get('team_members', []))
        content += self.format_metric("Team Size", f"{team_size} sales professionals")
        content += self.format_metric("New Hires (Last 90 Days)", str(team_data.get('new_hires', 0)))
        content += self.format_metric("Team Tenure (Average)", f"{team_data.get('avg_tenure', 18)} months")
        
        # Performance distribution
        content += "\n**Performance Distribution:**\n"
        performance_bands = team_data.get('performance_bands', {})
        total_team = sum(performance_bands.values()) or 1
        
        for band, count in performance_bands.items():
            percentage = (count / total_team) * 100
            emoji = {"exceeding": "🌟", "meeting": "✅", "developing": "🔄", "underperforming": "⚠️"}.get(band, "📊")
            content += f"- {emoji} {band.title()}: {count} reps ({percentage:.0f}%)\n"
        
        # Top performers
        top_performers = team_data.get('top_performers', [])
        if top_performers:
            content += "\n**Top Performers This Month:**\n"
            for performer in top_performers[:3]:
                quota_percent = performer.get('quota_attainment', 0)
                content += f"- {performer.get('name', 'Unknown')}: {quota_percent}% of quota\n"
        
        # Team health indicators
        content += "\n**Team Health Indicators:**\n"
        health_metrics = team_data.get('health_metrics', {})
        content += self.format_metric("Activity Compliance", f"{health_metrics.get('activity_compliance', 85)}%")
        content += self.format_metric("Pipeline Coverage", f"{health_metrics.get('pipeline_coverage', 3.2)}x quota")
        content += self.format_metric("Forecast Accuracy", f"{health_metrics.get('forecast_accuracy', 92)}%")
        
        return content
    
    def _analyze_pipeline_health(self, context: Dict[str, Any]) -> str:
        pipeline_data = context.get('pipeline_data', {})
        
        content = "### Pipeline Analysis\n\n"
        
        # Overall pipeline metrics
        total_pipeline = pipeline_data.get('total_value', 0)
        deal_count = pipeline_data.get('deal_count', 0)
        avg_deal_size = total_pipeline / max(1, deal_count)
        
        content += self.format_metric("Total Pipeline Value", self._format_currency(total_pipeline))
        content += self.format_metric("Active Opportunities", str(deal_count))
        content += self.format_metric("Average Deal Size", self._format_currency(avg_deal_size))
        
        # Pipeline by stage
        content += "\n**Pipeline Distribution:**\n"
        stage_data = pipeline_data.get('by_stage', {})
        for stage, data in stage_data.items():
            value = data.get('value', 0)
            count = data.get('count', 0)
            content += f"- {stage.title()}: {count} deals ({self._format_currency(value)})\n"
        
        # Pipeline velocity
        content += "\n**Pipeline Velocity:**\n"
        velocity_data = pipeline_data.get('velocity', {})
        content += self.format_metric("Average Sales Cycle", f"{velocity_data.get('avg_cycle_days', 45)} days")
        content += self.format_metric("Stage Progression Rate", f"{velocity_data.get('progression_rate', 75)}%")
        content += self.format_metric("Win Rate", f"{velocity_data.get('win_rate', 28)}%")
        
        # Pipeline quality indicators
        content += "\n**Quality Indicators:**\n"
        quality_data = pipeline_data.get('quality', {})
        
        # Stalled deals
        stalled_deals = quality_data.get('stalled_deals', 0)
        stalled_percentage = (stalled_deals / max(1, deal_count)) * 100
        stalled_status = "🔴" if stalled_percentage > 20 else "🟡" if stalled_percentage > 10 else "✅"
        content += f"- Stalled Deals (>14 days): {stalled_deals} ({stalled_percentage:.0f}%) {stalled_status}\n"
        
        # Single-threaded deals
        single_threaded = quality_data.get('single_threaded', 0)
        single_percentage = (single_threaded / max(1, deal_count)) * 100
        single_status = "🔴" if single_percentage > 30 else "🟡" if single_percentage > 15 else "✅"
        content += f"- Single-Threaded Deals: {single_threaded} ({single_percentage:.0f}%) {single_status}\n"
        
        # Champion identified
        champions = quality_data.get('with_champions', 0)
        champion_percentage = (champions / max(1, deal_count)) * 100
        champion_status = "✅" if champion_percentage > 70 else "🟡" if champion_percentage > 50 else "🔴"
        content += f"- Deals with Champions: {champions} ({champion_percentage:.0f}%) {champion_status}\n"
        
        return content
    
    def _track_quota_performance(self, context: Dict[str, Any]) -> str:
        quota_data = context.get('quota_data', {})
        
        content = "### Quota Performance\n\n"
        
        # Team quota summary
        team_quota = quota_data.get('team_quota', 0)
        team_achieved = quota_data.get('team_achieved', 0)
        team_percentage = (team_achieved / team_quota) * 100 if team_quota > 0 else 0
        
        content += self.format_metric("Team Quota", self._format_currency(team_quota))
        content += self.format_metric("Team Achievement", self._format_currency(team_achieved))
        content += self.format_metric("Team Attainment", f"{team_percentage:.1f}%")
        
        # Monthly progress
        current_month_day = datetime.now().day
        days_in_month = (datetime.now().replace(month=datetime.now().month + 1, day=1) - timedelta(days=1)).day
        month_progress = current_month_day / days_in_month
        
        content += f"\n**Monthly Progress ({current_month_day}/{days_in_month} days):**\n"
        expected_progress = month_progress * 100
        actual_progress = team_percentage
        
        if actual_progress >= expected_progress:
            status = "✅ On Track"
        elif actual_progress >= expected_progress * 0.9:
            status = "🟡 Slightly Behind"
        else:
            status = "🔴 Needs Attention"
        
        content += f"- Expected Progress: {expected_progress:.0f}%\n"
        content += f"- Actual Progress: {actual_progress:.1f}%\n"
        content += f"- Status: {status}\n"
        
        # Individual quota performance
        content += "\n**Individual Performance:**\n"
        individual_performance = quota_data.get('individual_performance', [])
        
        performance_buckets = {
            "Above 100%": 0,
            "90-100%": 0,
            "75-90%": 0,
            "Below 75%": 0
        }
        
        for rep in individual_performance:
            attainment = rep.get('quota_attainment', 0)
            if attainment >= 100:
                performance_buckets["Above 100%"] += 1
            elif attainment >= 90:
                performance_buckets["90-100%"] += 1
            elif attainment >= 75:
                performance_buckets["75-90%"] += 1
            else:
                performance_buckets["Below 75%"] += 1
        
        for bucket, count in performance_buckets.items():
            content += f"- {bucket}: {count} reps\n"
        
        return content
    
    def _analyze_sales_efficiency(self, context: Dict[str, Any]) -> str:
        efficiency_data = context.get('efficiency_data', {})
        
        content = "### Sales Efficiency Metrics\n\n"
        
        # Activity efficiency
        content += "**Activity Metrics:**\n"
        activity_data = efficiency_data.get('activities', {})
        content += self.format_metric("Average Calls/Rep/Day", str(activity_data.get('calls_per_day', 12)))
        content += self.format_metric("Email Response Rate", f"{activity_data.get('email_response_rate', 15)}%")
        content += self.format_metric("Demo-to-Opp Conversion", f"{activity_data.get('demo_conversion', 65)}%")
        content += self.format_metric("Meeting Show Rate", f"{activity_data.get('meeting_show_rate', 88)}%")
        
        # Conversion funnel
        content += "\n**Conversion Funnel:**\n"
        funnel_data = efficiency_data.get('funnel', {})
        content += self.format_metric("Lead to Qualified Opp", f"{funnel_data.get('lead_to_opp', 12)}%")
        content += self.format_metric("Opp to Demo", f"{funnel_data.get('opp_to_demo', 75)}%")
        content += self.format_metric("Demo to Proposal", f"{funnel_data.get('demo_to_proposal', 45)}%")
        content += self.format_metric("Proposal to Close", f"{funnel_data.get('proposal_to_close', 35)}%")
        
        # Time allocation
        content += "\n**Time Allocation Analysis:**\n"
        time_data = efficiency_data.get('time_allocation', {})
        content += f"- Selling Activities: {time_data.get('selling', 60)}%\n"
        content += f"- Administrative: {time_data.get('admin', 25)}%\n"
        content += f"- Training/Development: {time_data.get('training', 10)}%\n"
        content += f"- Internal Meetings: {time_data.get('meetings', 5)}%\n"
        
        # Productivity indicators
        content += "\n**Productivity Indicators:**\n"
        productivity_data = efficiency_data.get('productivity', {})
        
        revenue_per_rep = productivity_data.get('revenue_per_rep', 0)
        content += self.format_metric("Revenue per Rep", self._format_currency(revenue_per_rep))
        
        deals_per_rep = productivity_data.get('deals_per_rep', 0)
        content += self.format_metric("Deals Closed per Rep", f"{deals_per_rep:.1f}/month")
        
        pipeline_per_rep = productivity_data.get('pipeline_per_rep', 0)
        content += self.format_metric("Pipeline per Rep", self._format_currency(pipeline_per_rep))
        
        return content
    
    def _analyze_competitive_position(self, context: Dict[str, Any]) -> str:
        competitive_data = context.get('competitive_data', {})
        
        content = "### Competitive Analysis\n\n"
        
        # Win/loss analysis
        win_loss_data = competitive_data.get('win_loss', {})
        content += "**Win/Loss Summary:**\n"
        content += self.format_metric("Overall Win Rate", f"{win_loss_data.get('win_rate', 28)}%")
        content += self.format_metric("Deals Won", str(win_loss_data.get('won', 0)))
        content += self.format_metric("Deals Lost", str(win_loss_data.get('lost', 0)))
        content += self.format_metric("No Decision", str(win_loss_data.get('no_decision', 0)))
        
        # Top competitors
        content += "\n**Primary Competitors:**\n"
        competitors = competitive_data.get('competitors', [])
        for comp in competitors[:5]:
            name = comp.get('name', 'Unknown')
            encounters = comp.get('encounters', 0)
            win_rate = comp.get('win_rate_against', 0)
            content += f"- {name}: {encounters} encounters (Win rate: {win_rate}%)\n"
        
        # Loss reasons
        content += "\n**Primary Loss Reasons:**\n"
        loss_reasons = competitive_data.get('loss_reasons', {})
        for reason, count in loss_reasons.items():
            content += f"- {reason}: {count} instances\n"
        
        # Competitive strengths
        content += "\n**Our Competitive Advantages:**\n"
        advantages = competitive_data.get('advantages', [])
        for advantage in advantages:
            content += f"- ✅ {advantage}\n"
        
        return content
    
    def _generate_strategic_actions(self, context: Dict[str, Any]) -> str:
        content = "### Strategic Actions & Focus Areas\n\n"
        
        # Based on performance analysis
        quota_data = context.get('quota_data', {})
        pipeline_data = context.get('pipeline_data', {})
        team_data = context.get('team_data', {})
        
        actions = []
        
        # Quota performance actions
        team_percentage = (quota_data.get('team_achieved', 0) / quota_data.get('team_quota', 1)) * 100
        if team_percentage < 80:
            actions.append({
                'priority': 'Critical',
                'area': 'Quota Attainment',
                'action': 'Implement quota recovery plan',
                'details': 'Focus on closing Q4 pipeline and accelerating deal velocity'
            })
        
        # Pipeline quality actions
        quality_data = pipeline_data.get('quality', {})
        stalled_percentage = (quality_data.get('stalled_deals', 0) / max(1, pipeline_data.get('deal_count', 1))) * 100
        if stalled_percentage > 15:
            actions.append({
                'priority': 'High',
                'area': 'Pipeline Health',
                'action': 'Address stalled deals',
                'details': f'{quality_data.get("stalled_deals", 0)} deals need immediate attention'
            })
        
        # Team performance actions
        underperforming = team_data.get('performance_bands', {}).get('underperforming', 0)
        if underperforming > 0:
            actions.append({
                'priority': 'High',
                'area': 'Team Development',
                'action': 'Performance improvement plans',
                'details': f'{underperforming} reps need coaching and development'
            })
        
        # Competitive actions
        competitive_data = context.get('competitive_data', {})
        win_rate = competitive_data.get('win_loss', {}).get('win_rate', 0)
        if win_rate < 25:
            actions.append({
                'priority': 'Medium',
                'area': 'Competitive Position',
                'action': 'Strengthen competitive positioning',
                'details': 'Review battlecards and train team on competitive advantages'
            })
        
        # Format actions
        priority_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
        actions.sort(key=lambda x: priority_order.get(x['priority'], 5))
        
        for i, action in enumerate(actions[:5], 1):
            priority_emoji = {
                'Critical': '🔴',
                'High': '🟡', 
                'Medium': '🟠',
                'Low': '🟢'
            }.get(action['priority'], '⚫')
            
            content += f"**{i}. {priority_emoji} {action['action']}**\n"
            content += f"   - Area: {action['area']}\n"
            content += f"   - Priority: {action['priority']}\n"
            content += f"   - Details: {action['details']}\n\n"
        
        # Strategic initiatives
        content += "### Longer-Term Strategic Initiatives\n"
        content += "- **Sales Process Optimization**: Implement MEDDPICC qualification rigor\n"
        content += "- **Team Capacity Planning**: Hire 2 additional AEs for Q1 growth\n"
        content += "- **Competitive Intelligence**: Enhanced competitor tracking and response\n"
        content += "- **Customer Success Integration**: Improve expansion and renewal coordination\n"
        
        return content
    
    def _format_currency(self, amount: float) -> str:
        if amount >= 1000000:
            return f"${amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"${amount/1000:.0f}K"
        else:
            return f"${amount:.0f}"