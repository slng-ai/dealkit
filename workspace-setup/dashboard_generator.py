"""
Sales Dashboard Generator

Generates text-based dashboards in Claude-friendly format for sales performance tracking.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random
from collections import defaultdict


class TextDashboardGenerator:
    """Generate formatted text dashboards for sales metrics and performance."""
    
    def __init__(self):
        self.dashboard_width = 80
        self.section_separator = "═" * self.dashboard_width
        self.subsection_separator = "─" * self.dashboard_width
        
    def generate_sales_overview_dashboard(self, data: Dict[str, Any]) -> str:
        """Generate a comprehensive sales overview dashboard."""
        dashboard = []
        
        # Header
        dashboard.append(self._generate_header("Sales Overview Dashboard"))
        dashboard.append(self._generate_timestamp())
        dashboard.append("")
        
        # Executive Summary
        dashboard.append(self._generate_executive_summary(data))
        dashboard.append(self.subsection_separator)
        
        # Pipeline Health
        dashboard.append(self._generate_pipeline_health(data.get('pipeline', {})))
        dashboard.append(self.subsection_separator)
        
        # Team Performance
        dashboard.append(self._generate_team_performance(data.get('team', {})))
        dashboard.append(self.subsection_separator)
        
        # Activity Metrics
        dashboard.append(self._generate_activity_metrics(data.get('activities', {})))
        dashboard.append(self.subsection_separator)
        
        # Customer Health
        dashboard.append(self._generate_customer_health(data.get('customers', {})))
        dashboard.append(self.subsection_separator)
        
        # Forecast Analysis
        dashboard.append(self._generate_forecast_analysis(data.get('forecast', {})))
        
        return "\n".join(dashboard)
    
    def generate_individual_dashboard(self, rep_name: str, data: Dict[str, Any]) -> str:
        """Generate individual sales rep dashboard."""
        dashboard = []
        
        # Header
        dashboard.append(self._generate_header(f"Individual Performance: {rep_name}"))
        dashboard.append(self._generate_timestamp())
        dashboard.append("")
        
        # Personal Metrics
        dashboard.append(self._generate_personal_metrics(data))
        dashboard.append(self.subsection_separator)
        
        # Pipeline Status
        dashboard.append(self._generate_personal_pipeline(data.get('pipeline', {})))
        dashboard.append(self.subsection_separator)
        
        # Activity Summary
        dashboard.append(self._generate_activity_summary(data.get('activities', {})))
        dashboard.append(self.subsection_separator)
        
        # Key Opportunities
        dashboard.append(self._generate_key_opportunities(data.get('opportunities', [])))
        dashboard.append(self.subsection_separator)
        
        # Action Items
        dashboard.append(self._generate_action_items(data.get('actions', [])))
        
        return "\n".join(dashboard)
    
    def generate_pipeline_dashboard(self, data: Dict[str, Any]) -> str:
        """Generate detailed pipeline analysis dashboard."""
        dashboard = []
        
        # Header
        dashboard.append(self._generate_header("Pipeline Analysis Dashboard"))
        dashboard.append(self._generate_timestamp())
        dashboard.append("")
        
        # Pipeline Summary
        dashboard.append(self._generate_pipeline_summary(data))
        dashboard.append(self.subsection_separator)
        
        # Stage Analysis
        dashboard.append(self._generate_stage_analysis(data.get('stages', {})))
        dashboard.append(self.subsection_separator)
        
        # Deal Velocity
        dashboard.append(self._generate_deal_velocity(data.get('velocity', {})))
        dashboard.append(self.subsection_separator)
        
        # Risk Analysis
        dashboard.append(self._generate_risk_analysis(data.get('risks', [])))
        dashboard.append(self.subsection_separator)
        
        # Win/Loss Trends
        dashboard.append(self._generate_win_loss_analysis(data.get('win_loss', {})))
        
        return "\n".join(dashboard)
    
    def _generate_header(self, title: str) -> str:
        """Generate dashboard header."""
        header = []
        header.append(self.section_separator)
        header.append(title.center(self.dashboard_width))
        header.append(self.section_separator)
        return "\n".join(header)
    
    def _generate_timestamp(self) -> str:
        """Generate timestamp line."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        period = f"Period: {(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}"
        return f"{timestamp} | {period}".center(self.dashboard_width)
    
    def _generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate executive summary section."""
        summary = ["📊 EXECUTIVE SUMMARY", ""]
        
        # Key metrics with visual indicators
        metrics = data.get('key_metrics', {})
        
        summary.append("Key Performance Indicators:")
        summary.append(f"  • Revenue (QTD):     ${metrics.get('revenue_qtd', 0):,.0f} "
                      f"({self._trend_indicator(metrics.get('revenue_trend', 0))})")
        summary.append(f"  • Pipeline Value:    ${metrics.get('pipeline_value', 0):,.0f} "
                      f"({metrics.get('pipeline_coverage', 0):.1f}x coverage)")
        summary.append(f"  • Win Rate:          {metrics.get('win_rate', 0):.1%} "
                      f"({self._trend_indicator(metrics.get('win_rate_trend', 0))})")
        summary.append(f"  • Avg Deal Size:     ${metrics.get('avg_deal_size', 0):,.0f} "
                      f"({self._trend_indicator(metrics.get('deal_size_trend', 0))})")
        summary.append(f"  • Sales Cycle:       {metrics.get('avg_sales_cycle', 0)} days "
                      f"({self._trend_indicator(metrics.get('cycle_trend', 0), reverse=True)})")
        
        return "\n".join(summary)
    
    def _generate_pipeline_health(self, pipeline_data: Dict[str, Any]) -> str:
        """Generate pipeline health visualization."""
        health = ["📈 PIPELINE HEALTH", ""]
        
        # Pipeline funnel visualization
        stages = pipeline_data.get('stages', {})
        if stages:
            health.append("Pipeline Funnel:")
            health.append("")
            
            max_value = max(stages.values()) if stages else 1
            for stage, value in stages.items():
                bar_length = int((value / max_value) * 50)
                bar = "█" * bar_length
                health.append(f"  {stage:<20} {bar:<50} ${value:,.0f}")
        
        # Health indicators
        health.append("")
        health.append("Health Indicators:")
        health_score = pipeline_data.get('health_score', 0)
        health.append(f"  • Overall Health:    {self._health_indicator(health_score)} ({health_score}/100)")
        health.append(f"  • Stage Velocity:    {pipeline_data.get('velocity_rating', 'Good')}")
        health.append(f"  • Deal Quality:      {pipeline_data.get('quality_score', 0)}/5 ⭐")
        health.append(f"  • Coverage Ratio:    {pipeline_data.get('coverage_ratio', 0):.1f}x")
        
        return "\n".join(health)
    
    def _generate_team_performance(self, team_data: Dict[str, Any]) -> str:
        """Generate team performance metrics."""
        performance = ["👥 TEAM PERFORMANCE", ""]
        
        # Top performers
        top_performers = team_data.get('top_performers', [])
        if top_performers:
            performance.append("Top Performers (QTD):")
            for i, performer in enumerate(top_performers[:5], 1):
                performance.append(f"  {i}. {performer['name']:<20} ${performer['revenue']:,.0f} "
                                 f"({performer['attainment']:.0%} of quota)")
        
        # Team metrics
        performance.append("")
        performance.append("Team Metrics:")
        performance.append(f"  • Team Attainment:   {team_data.get('team_attainment', 0):.0%} of target")
        performance.append(f"  • Active Reps:       {team_data.get('active_reps', 0)} / {team_data.get('total_reps', 0)}")
        performance.append(f"  • Avg Attainment:    {team_data.get('avg_attainment', 0):.0%}")
        performance.append(f"  • Ramp Progress:     {team_data.get('ramp_progress', 0)} new reps on track")
        
        return "\n".join(performance)
    
    def _generate_activity_metrics(self, activity_data: Dict[str, Any]) -> str:
        """Generate activity metrics section."""
        activities = ["📞 ACTIVITY METRICS", ""]
        
        # Activity grid
        activities.append("Weekly Activity Summary:")
        activities.append("┌─────────────────┬──────────┬──────────┬──────────┬──────────┐")
        activities.append("│ Metric          │ This Week│ Last Week│  Trend   │  Target  │")
        activities.append("├─────────────────┼──────────┼──────────┼──────────┼──────────┤")
        
        metrics = [
            ('Calls', 'calls'),
            ('Emails', 'emails'),
            ('Meetings', 'meetings'),
            ('Demos', 'demos'),
            ('Proposals', 'proposals')
        ]
        
        for label, key in metrics:
            this_week = activity_data.get(f'{key}_this_week', 0)
            last_week = activity_data.get(f'{key}_last_week', 0)
            target = activity_data.get(f'{key}_target', 0)
            trend = self._calculate_trend(this_week, last_week)
            
            activities.append(f"│ {label:<15} │ {this_week:>8} │ {last_week:>8} │ {trend:>8} │ {target:>8} │")
        
        activities.append("└─────────────────┴──────────┴──────────┴──────────┴──────────┘")
        
        return "\n".join(activities)
    
    def _generate_customer_health(self, customer_data: Dict[str, Any]) -> str:
        """Generate customer health summary."""
        health = ["🏥 CUSTOMER HEALTH", ""]
        
        # Health distribution
        distribution = customer_data.get('health_distribution', {})
        if distribution:
            health.append("Health Score Distribution:")
            total = sum(distribution.values())
            for status, count in distribution.items():
                percentage = (count / total * 100) if total > 0 else 0
                bar_length = int(percentage / 2)
                bar = "█" * bar_length
                health.append(f"  {status:<12} {bar:<40} {count} ({percentage:.0f}%)")
        
        # At-risk accounts
        at_risk = customer_data.get('at_risk_accounts', [])
        if at_risk:
            health.append("")
            health.append("⚠️  At-Risk Accounts:")
            for account in at_risk[:5]:
                health.append(f"  • {account['name']:<30} - {account['risk_reason']}")
        
        return "\n".join(health)
    
    def _generate_forecast_analysis(self, forecast_data: Dict[str, Any]) -> str:
        """Generate forecast analysis section."""
        forecast = ["📅 FORECAST ANALYSIS", ""]
        
        # Current quarter forecast
        forecast.append("Current Quarter Forecast:")
        forecast.append(f"  • Closed:      ${forecast_data.get('closed', 0):,.0f}")
        forecast.append(f"  • Commit:      ${forecast_data.get('commit', 0):,.0f}")
        forecast.append(f"  • Best Case:   ${forecast_data.get('best_case', 0):,.0f}")
        forecast.append(f"  • Pipeline:    ${forecast_data.get('pipeline', 0):,.0f}")
        forecast.append(f"  • Target:      ${forecast_data.get('target', 0):,.0f}")
        
        # Forecast confidence
        confidence = forecast_data.get('confidence', 0)
        forecast.append("")
        forecast.append(f"Forecast Confidence: {self._confidence_bar(confidence)} {confidence}%")
        
        # Key deals
        key_deals = forecast_data.get('key_deals', [])
        if key_deals:
            forecast.append("")
            forecast.append("🎯 Key Deals to Watch:")
            for deal in key_deals[:5]:
                forecast.append(f"  • {deal['name']:<25} ${deal['amount']:,.0f} - {deal['stage']} ({deal['close_date']})")
        
        return "\n".join(forecast)
    
    def _generate_personal_metrics(self, data: Dict[str, Any]) -> str:
        """Generate personal performance metrics."""
        metrics = ["📊 PERSONAL PERFORMANCE", ""]
        
        # Quota attainment visualization
        attainment = data.get('quota_attainment', 0)
        quota_bar = self._progress_bar(attainment, 100)
        metrics.append(f"Quota Attainment: {quota_bar} {attainment:.0%}")
        
        # Key metrics
        metrics.append("")
        metrics.append("Key Metrics (QTD):")
        metrics.append(f"  • Revenue Closed:    ${data.get('revenue_closed', 0):,.0f}")
        metrics.append(f"  • Pipeline Created:  ${data.get('pipeline_created', 0):,.0f}")
        metrics.append(f"  • Deals Closed:      {data.get('deals_closed', 0)}")
        metrics.append(f"  • Win Rate:          {data.get('win_rate', 0):.1%}")
        metrics.append(f"  • Avg Deal Size:     ${data.get('avg_deal_size', 0):,.0f}")
        
        return "\n".join(metrics)
    
    def _generate_personal_pipeline(self, pipeline_data: Dict[str, Any]) -> str:
        """Generate personal pipeline summary."""
        pipeline = ["📈 MY PIPELINE", ""]
        
        # Pipeline by stage
        stages = pipeline_data.get('stages', {})
        total_pipeline = sum(stages.values()) if stages else 0
        
        pipeline.append(f"Total Pipeline Value: ${total_pipeline:,.0f}")
        pipeline.append("")
        
        for stage, value in stages.items():
            percentage = (value / total_pipeline * 100) if total_pipeline > 0 else 0
            pipeline.append(f"  {stage:<20} ${value:>12,.0f} ({percentage:>5.1f}%)")
        
        # Pipeline health
        pipeline.append("")
        pipeline.append("Pipeline Health:")
        pipeline.append(f"  • Coverage Ratio:    {pipeline_data.get('coverage_ratio', 0):.1f}x")
        pipeline.append(f"  • Deals at Risk:     {pipeline_data.get('deals_at_risk', 0)}")
        pipeline.append(f"  • Next 30 Days:      ${pipeline_data.get('next_30_days', 0):,.0f}")
        
        return "\n".join(pipeline)
    
    def _generate_activity_summary(self, activity_data: Dict[str, Any]) -> str:
        """Generate personal activity summary."""
        activities = ["📞 ACTIVITY SUMMARY", ""]
        
        # This week's activities
        activities.append("This Week's Activities:")
        activities.append(f"  • Calls Made:        {activity_data.get('calls', 0)} / {activity_data.get('calls_target', 0)}")
        activities.append(f"  • Emails Sent:       {activity_data.get('emails', 0)} / {activity_data.get('emails_target', 0)}")
        activities.append(f"  • Meetings Held:     {activity_data.get('meetings', 0)} / {activity_data.get('meetings_target', 0)}")
        activities.append(f"  • Demos Delivered:   {activity_data.get('demos', 0)} / {activity_data.get('demos_target', 0)}")
        
        # Activity score
        score = activity_data.get('activity_score', 0)
        activities.append("")
        activities.append(f"Activity Score: {self._activity_score_visual(score)} {score}/100")
        
        return "\n".join(activities)
    
    def _generate_key_opportunities(self, opportunities: List[Dict[str, Any]]) -> str:
        """Generate key opportunities section."""
        opps = ["🎯 KEY OPPORTUNITIES", ""]
        
        if not opportunities:
            opps.append("No key opportunities to display.")
            return "\n".join(opps)
        
        opps.append("Top Opportunities by Value:")
        for i, opp in enumerate(opportunities[:5], 1):
            close_date = opp.get('close_date', 'TBD')
            stage = opp.get('stage', 'Unknown')
            opps.append(f"  {i}. {opp['name'][:40]:<40}")
            opps.append(f"     ${opp['amount']:,.0f} | {stage} | Close: {close_date}")
            opps.append("")
        
        return "\n".join(opps[:-1])  # Remove last empty line
    
    def _generate_action_items(self, actions: List[Dict[str, Any]]) -> str:
        """Generate action items section."""
        items = ["✅ ACTION ITEMS", ""]
        
        if not actions:
            items.append("No pending action items.")
            return "\n".join(items)
        
        # Group by priority
        high_priority = [a for a in actions if a.get('priority') == 'high']
        normal_priority = [a for a in actions if a.get('priority') != 'high']
        
        if high_priority:
            items.append("🔴 High Priority:")
            for action in high_priority[:3]:
                items.append(f"  • {action['description']}")
                items.append(f"    Due: {action.get('due_date', 'ASAP')}")
        
        if normal_priority:
            items.append("")
            items.append("🟡 Normal Priority:")
            for action in normal_priority[:3]:
                items.append(f"  • {action['description']}")
        
        return "\n".join(items)
    
    def _generate_pipeline_summary(self, data: Dict[str, Any]) -> str:
        """Generate pipeline summary section."""
        summary = ["📊 PIPELINE SUMMARY", ""]
        
        # Total pipeline metrics
        summary.append(f"Total Pipeline Value: ${data.get('total_value', 0):,.0f}")
        summary.append(f"Number of Deals: {data.get('deal_count', 0)}")
        summary.append(f"Average Deal Size: ${data.get('avg_deal_size', 0):,.0f}")
        summary.append(f"Pipeline Coverage: {data.get('coverage_ratio', 0):.1f}x of target")
        
        # Pipeline quality
        summary.append("")
        summary.append("Pipeline Quality Metrics:")
        summary.append(f"  • Qualified Deals:   {data.get('qualified_percentage', 0):.0%}")
        summary.append(f"  • Multi-threaded:    {data.get('multithreaded_percentage', 0):.0%}")
        summary.append(f"  • Has Champion:      {data.get('champion_percentage', 0):.0%}")
        summary.append(f"  • Next Steps Set:    {data.get('next_steps_percentage', 0):.0%}")
        
        return "\n".join(summary)
    
    def _generate_stage_analysis(self, stages: Dict[str, Dict[str, Any]]) -> str:
        """Generate stage-by-stage analysis."""
        analysis = ["📈 STAGE ANALYSIS", ""]
        
        # Stage conversion metrics
        analysis.append("Stage Conversion Rates:")
        for stage_name, metrics in stages.items():
            conversion_rate = metrics.get('conversion_rate', 0)
            avg_days = metrics.get('avg_days', 0)
            count = metrics.get('count', 0)
            value = metrics.get('value', 0)
            
            analysis.append(f"\n{stage_name}:")
            analysis.append(f"  • Deals: {count} (${value:,.0f})")
            analysis.append(f"  • Conversion: {conversion_rate:.0%}")
            analysis.append(f"  • Avg Time: {avg_days} days")
        
        return "\n".join(analysis)
    
    def _generate_deal_velocity(self, velocity_data: Dict[str, Any]) -> str:
        """Generate deal velocity metrics."""
        velocity = ["⚡ DEAL VELOCITY", ""]
        
        # Average sales cycle
        velocity.append(f"Average Sales Cycle: {velocity_data.get('avg_sales_cycle', 0)} days")
        velocity.append("")
        
        # Velocity by deal size
        velocity.append("Sales Cycle by Deal Size:")
        size_categories = velocity_data.get('by_size', {})
        for size, days in size_categories.items():
            velocity.append(f"  • {size:<15} {days} days")
        
        # Velocity trends
        velocity.append("")
        velocity.append("Velocity Trends:")
        velocity.append(f"  • This Quarter:     {velocity_data.get('current_quarter', 0)} days")
        velocity.append(f"  • Last Quarter:     {velocity_data.get('last_quarter', 0)} days")
        velocity.append(f"  • Trend:            {self._trend_indicator(velocity_data.get('trend', 0), reverse=True)}")
        
        return "\n".join(velocity)
    
    def _generate_risk_analysis(self, risks: List[Dict[str, Any]]) -> str:
        """Generate risk analysis section."""
        risk_analysis = ["⚠️  RISK ANALYSIS", ""]
        
        if not risks:
            risk_analysis.append("No significant risks identified.")
            return "\n".join(risk_analysis)
        
        # Group by risk type
        risk_groups = defaultdict(list)
        for risk in risks:
            risk_groups[risk.get('type', 'Other')].append(risk)
        
        for risk_type, risk_list in risk_groups.items():
            risk_analysis.append(f"\n{risk_type} Risks:")
            for risk in risk_list[:3]:
                risk_analysis.append(f"  • {risk['deal_name']}: {risk['description']}")
                risk_analysis.append(f"    Impact: ${risk.get('amount', 0):,.0f} | Action: {risk.get('mitigation', 'Review needed')}")
        
        return "\n".join(risk_analysis)
    
    def _generate_win_loss_analysis(self, win_loss_data: Dict[str, Any]) -> str:
        """Generate win/loss analysis."""
        analysis = ["🏆 WIN/LOSS ANALYSIS", ""]
        
        # Win rate visualization
        win_rate = win_loss_data.get('win_rate', 0)
        win_bar = self._win_rate_visual(win_rate)
        analysis.append(f"Overall Win Rate: {win_bar} {win_rate:.0%}")
        
        # Win/loss reasons
        analysis.append("")
        analysis.append("Top Win Reasons:")
        for reason in win_loss_data.get('win_reasons', [])[:3]:
            analysis.append(f"  • {reason['reason']} ({reason['count']} deals)")
        
        analysis.append("")
        analysis.append("Top Loss Reasons:")
        for reason in win_loss_data.get('loss_reasons', [])[:3]:
            analysis.append(f"  • {reason['reason']} ({reason['count']} deals)")
        
        # Competitive win rates
        analysis.append("")
        analysis.append("Competitive Win Rates:")
        for competitor, rate in win_loss_data.get('competitive_rates', {}).items():
            analysis.append(f"  • vs {competitor}: {rate:.0%}")
        
        return "\n".join(analysis)
    
    # Helper methods for visual elements
    def _trend_indicator(self, value: float, reverse: bool = False) -> str:
        """Generate trend indicator arrow."""
        if reverse:
            value = -value
        
        if value > 10:
            return "↑↑ +" + f"{abs(value):.0f}%"
        elif value > 0:
            return "↑ +" + f"{value:.0f}%"
        elif value < -10:
            return "↓↓ " + f"{value:.0f}%"
        elif value < 0:
            return "↓ " + f"{value:.0f}%"
        else:
            return "→ 0%"
    
    def _health_indicator(self, score: int) -> str:
        """Generate health indicator emoji."""
        if score >= 80:
            return "🟢 Excellent"
        elif score >= 60:
            return "🟡 Good"
        elif score >= 40:
            return "🟠 Fair"
        else:
            return "🔴 Poor"
    
    def _progress_bar(self, current: float, target: float, width: int = 20) -> str:
        """Generate a progress bar."""
        percentage = min(current / target, 1.0) if target > 0 else 0
        filled = int(percentage * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"
    
    def _confidence_bar(self, confidence: float, width: int = 20) -> str:
        """Generate confidence visualization."""
        filled = int((confidence / 100) * width)
        bar = "▰" * filled + "▱" * (width - filled)
        return bar
    
    def _activity_score_visual(self, score: int) -> str:
        """Generate activity score visualization."""
        stars = int(score / 20)
        return "⭐" * stars + "☆" * (5 - stars)
    
    def _win_rate_visual(self, rate: float) -> str:
        """Generate win rate visualization."""
        wins = int(rate * 10)
        losses = 10 - wins
        return "🟢" * wins + "🔴" * losses
    
    def _calculate_trend(self, current: float, previous: float) -> str:
        """Calculate and format trend."""
        if previous == 0:
            return "N/A"
        
        change = ((current - previous) / previous) * 100
        if change > 0:
            return f"↑{change:.0f}%"
        elif change < 0:
            return f"↓{abs(change):.0f}%"
        else:
            return "→0%"


# Example usage function
def generate_sample_dashboards():
    """Generate sample dashboards with mock data."""
    generator = TextDashboardGenerator()
    
    # Sample data for sales overview dashboard
    overview_data = {
        'key_metrics': {
            'revenue_qtd': 2500000,
            'revenue_trend': 15,
            'pipeline_value': 5000000,
            'pipeline_coverage': 3.2,
            'win_rate': 0.28,
            'win_rate_trend': 5,
            'avg_deal_size': 85000,
            'deal_size_trend': -3,
            'avg_sales_cycle': 45,
            'cycle_trend': -10
        },
        'pipeline': {
            'stages': {
                'Discovery': 1500000,
                'Technical Validation': 1200000,
                'Business Case': 800000,
                'Negotiation': 500000,
                'Closing': 200000
            },
            'health_score': 75,
            'velocity_rating': 'Good',
            'quality_score': 4.2,
            'coverage_ratio': 3.2
        },
        'team': {
            'top_performers': [
                {'name': 'Sarah Johnson', 'revenue': 450000, 'attainment': 1.12},
                {'name': 'Mike Chen', 'revenue': 380000, 'attainment': 0.95},
                {'name': 'Emily Davis', 'revenue': 350000, 'attainment': 0.88}
            ],
            'team_attainment': 0.92,
            'active_reps': 12,
            'total_reps': 15,
            'avg_attainment': 0.85,
            'ramp_progress': 3
        },
        'activities': {
            'calls_this_week': 325,
            'calls_last_week': 290,
            'calls_target': 300,
            'emails_this_week': 650,
            'emails_last_week': 600,
            'emails_target': 600,
            'meetings_this_week': 48,
            'meetings_last_week': 52,
            'meetings_target': 50,
            'demos_this_week': 12,
            'demos_last_week': 10,
            'demos_target': 15,
            'proposals_this_week': 5,
            'proposals_last_week': 8,
            'proposals_target': 6
        },
        'customers': {
            'health_distribution': {
                'Excellent': 45,
                'Good': 120,
                'Fair': 65,
                'Poor': 20
            },
            'at_risk_accounts': [
                {'name': 'TechCorp', 'risk_reason': 'No engagement in 30 days'},
                {'name': 'DataFlow Inc', 'risk_reason': 'Champion left company'}
            ]
        },
        'forecast': {
            'closed': 1200000,
            'commit': 800000,
            'best_case': 600000,
            'pipeline': 400000,
            'target': 3000000,
            'confidence': 85,
            'key_deals': [
                {'name': 'MegaCorp', 'amount': 250000, 'stage': 'Negotiation', 'close_date': '2024-03-15'},
                {'name': 'StartupXYZ', 'amount': 150000, 'stage': 'Business Case', 'close_date': '2024-03-28'}
            ]
        }
    }
    
    # Generate and return the dashboard
    return generator.generate_sales_overview_dashboard(overview_data)


if __name__ == "__main__":
    # Generate sample dashboard
    dashboard = generate_sample_dashboards()
    print(dashboard)