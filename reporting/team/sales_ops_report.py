from ..base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class SalesOpsReport(BaseReport):
    """Sales Operations Report - Process efficiency, data quality, and forecasting accuracy"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Process Efficiency Analysis
        report += self.format_section(
            "Sales Process Efficiency",
            self._analyze_process_efficiency(context)
        )
        
        # Data Quality Assessment
        report += self.format_section(
            "CRM Data Quality & Hygiene",
            self._assess_data_quality(context)
        )
        
        # Forecasting Accuracy
        report += self.format_section(
            "Forecast Accuracy Analysis",
            self._analyze_forecast_accuracy(context)
        )
        
        # Conversion Funnel Analysis
        report += self.format_section(
            "Sales Funnel Performance",
            self._analyze_conversion_funnel(context)
        )
        
        # Tool Utilization
        report += self.format_section(
            "Sales Tool Adoption & ROI",
            self._analyze_tool_utilization(context)
        )
        
        # Operational Recommendations
        report += self.format_section(
            "Process Optimization Recommendations",
            self._generate_optimization_recommendations(context)
        )
        
        return report
    
    def _analyze_process_efficiency(self, context: Dict[str, Any]) -> str:
        process_data = context.get('process_data', {})
        
        content = "### Sales Process Metrics\n\n"
        
        # Sales velocity metrics
        velocity_data = process_data.get('velocity', {})
        content += "**Sales Velocity Analysis:**\n"
        content += self.format_metric("Average Sales Cycle", f"{velocity_data.get('avg_cycle_days', 45)} days")
        content += self.format_metric("Median Sales Cycle", f"{velocity_data.get('median_cycle_days', 38)} days")
        content += self.format_metric("Cycle Variance", f"±{velocity_data.get('cycle_variance', 15)} days")
        
        # Stage progression efficiency
        content += "\n**Stage Progression Times:**\n"
        stage_times = velocity_data.get('stage_times', {})
        benchmarks = {
            'discovery': 14,
            'technical_validation': 21,
            'business_case': 14,
            'negotiation': 14,
            'closed_won': 7
        }
        
        for stage, actual_days in stage_times.items():
            benchmark = benchmarks.get(stage, 14)
            variance = actual_days - benchmark
            status = "✅" if variance <= 0 else "🟡" if variance <= 7 else "🔴"
            
            content += f"- {stage.title()}: {actual_days} days (benchmark: {benchmark}) {status}\n"
            if variance > 0:
                content += f"  - {variance} days slower than benchmark\n"
        
        # Activity efficiency
        content += "\n**Activity Efficiency:**\n"
        activity_data = process_data.get('activities', {})
        content += self.format_metric("Calls per Day (Team Avg)", str(activity_data.get('calls_per_day', 12)))
        content += self.format_metric("Email Response Rate", f"{activity_data.get('email_response_rate', 15)}%")
        content += self.format_metric("Meeting Show Rate", f"{activity_data.get('meeting_show_rate', 88)}%")
        content += self.format_metric("Demo Conversion Rate", f"{activity_data.get('demo_conversion', 65)}%")
        
        # Process bottlenecks
        content += "\n**Identified Bottlenecks:**\n"
        bottlenecks = process_data.get('bottlenecks', [])
        if bottlenecks:
            for bottleneck in bottlenecks:
                stage = bottleneck.get('stage', 'Unknown')
                impact = bottleneck.get('impact', 'Medium')
                deals_affected = bottleneck.get('deals_affected', 0)
                
                impact_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(impact, "⚫")
                content += f"- {impact_emoji} {stage}: {deals_affected} deals affected\n"
        else:
            content += "- ✅ No significant bottlenecks identified\n"
        
        return content
    
    def _assess_data_quality(self, context: Dict[str, Any]) -> str:
        data_quality = context.get('data_quality', {})
        
        content = "### CRM Data Quality Dashboard\n\n"
        
        # Overall data health score
        overall_score = data_quality.get('overall_score', 85)
        score_status = "✅" if overall_score >= 90 else "🟡" if overall_score >= 80 else "🔴"
        content += f"**Overall Data Quality Score: {overall_score}/100 {score_status}**\n\n"
        
        # Contact data quality
        contact_quality = data_quality.get('contact_quality', {})
        content += "**Contact Data Quality:**\n"
        content += self.format_metric("Complete Contact Profiles", f"{contact_quality.get('complete_profiles', 85)}%")
        content += self.format_metric("Verified Email Addresses", f"{contact_quality.get('verified_emails', 92)}%")
        content += self.format_metric("Phone Numbers Present", f"{contact_quality.get('phone_numbers', 78)}%")
        content += self.format_metric("LinkedIn Profiles Linked", f"{contact_quality.get('linkedin_profiles', 65)}%")
        
        # Opportunity data quality
        opp_quality = data_quality.get('opportunity_quality', {})
        content += "\n**Opportunity Data Quality:**\n"
        content += self.format_metric("Next Steps Defined", f"{opp_quality.get('next_steps_defined', 82)}%")
        content += self.format_metric("Close Dates Set", f"{opp_quality.get('close_dates_set', 95)}%")
        content += self.format_metric("Deal Size Estimates", f"{opp_quality.get('deal_sizes', 88)}%")
        content += self.format_metric("Stage Progression Logic", f"{opp_quality.get('stage_logic', 91)}%")
        
        # Activity logging
        activity_quality = data_quality.get('activity_quality', {})
        content += "\n**Activity Logging Quality:**\n"
        content += self.format_metric("Activities Logged Daily", f"{activity_quality.get('daily_logging', 76)}%")
        content += self.format_metric("Call Outcomes Recorded", f"{activity_quality.get('call_outcomes', 84)}%")
        content += self.format_metric("Email Opens Tracked", f"{activity_quality.get('email_tracking', 91)}%")
        content += self.format_metric("Meeting Notes Present", f"{activity_quality.get('meeting_notes', 69)}%")
        
        # Data hygiene issues
        content += "\n**Data Hygiene Issues:**\n"
        hygiene_issues = data_quality.get('hygiene_issues', {})
        
        duplicate_contacts = hygiene_issues.get('duplicate_contacts', 0)
        if duplicate_contacts > 0:
            content += f"- 🟡 {duplicate_contacts} potential duplicate contacts found\n"
        
        stale_opps = hygiene_issues.get('stale_opportunities', 0)
        if stale_opps > 0:
            content += f"- 🔴 {stale_opps} opportunities not updated in >30 days\n"
        
        missing_owners = hygiene_issues.get('missing_owners', 0)
        if missing_owners > 0:
            content += f"- 🔴 {missing_owners} records without assigned owners\n"
        
        if not any([duplicate_contacts, stale_opps, missing_owners]):
            content += "- ✅ No major data hygiene issues identified\n"
        
        return content
    
    def _analyze_forecast_accuracy(self, context: Dict[str, Any]) -> str:
        forecast_data = context.get('forecast_data', {})
        
        content = "### Forecast Accuracy Analysis\n\n"
        
        # Overall accuracy metrics
        content += "**Quarterly Forecast Accuracy:**\n"
        quarterly_accuracy = forecast_data.get('quarterly_accuracy', {})
        
        for quarter, accuracy in quarterly_accuracy.items():
            status = "✅" if accuracy >= 95 else "🟡" if accuracy >= 90 else "🔴"
            content += f"- {quarter}: {accuracy}% {status}\n"
        
        # Forecast category accuracy
        content += "\n**Forecast Category Performance:**\n"
        category_accuracy = forecast_data.get('category_accuracy', {})
        
        categories = ['Closed', 'Commit', 'Best Case', 'Pipeline']
        for category in categories:
            accuracy = category_accuracy.get(category.lower(), 0)
            content += f"- {category}: {accuracy}% accuracy\n"
        
        # Individual rep accuracy
        content += "\n**Individual Forecast Accuracy:**\n"
        individual_accuracy = forecast_data.get('individual_accuracy', [])
        
        # Group by accuracy ranges
        accuracy_buckets = {">95%": 0, "90-95%": 0, "85-90%": 0, "<85%": 0}
        
        for rep_data in individual_accuracy:
            accuracy = rep_data.get('accuracy', 0)
            if accuracy >= 95:
                accuracy_buckets[">95%"] += 1
            elif accuracy >= 90:
                accuracy_buckets["90-95%"] += 1
            elif accuracy >= 85:
                accuracy_buckets["85-90%"] += 1
            else:
                accuracy_buckets["<85%"] += 1
        
        for bucket, count in accuracy_buckets.items():
            content += f"- {bucket}: {count} reps\n"
        
        # Common forecast issues
        content += "\n**Common Forecast Issues:**\n"
        forecast_issues = forecast_data.get('issues', [])
        if forecast_issues:
            for issue in forecast_issues:
                frequency = issue.get('frequency', 0)
                description = issue.get('description', 'Unknown issue')
                content += f"- {description}: {frequency} instances\n"
        else:
            content += "- ✅ No recurring forecast issues identified\n"
        
        # Accuracy trends
        content += "\n**Forecast Accuracy Trends:**\n"
        trends = forecast_data.get('trends', {})
        trend_direction = trends.get('direction', 'stable')
        trend_magnitude = trends.get('magnitude', 0)
        
        if trend_direction == 'improving':
            content += f"📈 Accuracy improving by {trend_magnitude}% over last quarter\n"
        elif trend_direction == 'declining':
            content += f"📉 Accuracy declining by {trend_magnitude}% - needs attention\n"
        else:
            content += f"↔️ Accuracy stable at current levels\n"
        
        return content
    
    def _analyze_conversion_funnel(self, context: Dict[str, Any]) -> str:
        funnel_data = context.get('funnel_data', {})
        
        content = "### Sales Funnel Conversion Analysis\n\n"
        
        # Overall funnel metrics
        content += "**Conversion Rates by Stage:**\n"
        conversions = funnel_data.get('conversions', {})
        
        funnel_stages = [
            ('Lead to Qualified Opportunity', 'lead_to_opp'),
            ('Opportunity to Demo', 'opp_to_demo'),
            ('Demo to Proposal', 'demo_to_proposal'),
            ('Proposal to Close', 'proposal_to_close'),
            ('Overall Lead to Close', 'lead_to_close')
        ]
        
        for stage_name, stage_key in funnel_stages:
            rate = conversions.get(stage_key, 0)
            # Benchmark conversion rates
            benchmarks = {
                'lead_to_opp': 15,
                'opp_to_demo': 70,
                'demo_to_proposal': 45,
                'proposal_to_close': 35,
                'lead_to_close': 2
            }
            
            benchmark = benchmarks.get(stage_key, 0)
            variance = rate - benchmark
            status = "✅" if variance >= 0 else "🔴"
            
            content += f"- {stage_name}: {rate}% (benchmark: {benchmark}%) {status}\n"
        
        # Volume analysis
        content += "\n**Funnel Volume Analysis:**\n"
        volumes = funnel_data.get('volumes', {})
        content += self.format_metric("Leads Generated", str(volumes.get('leads', 0)))
        content += self.format_metric("Qualified Opportunities", str(volumes.get('opportunities', 0)))
        content += self.format_metric("Demos Scheduled", str(volumes.get('demos', 0)))
        content += self.format_metric("Proposals Sent", str(volumes.get('proposals', 0)))
        content += self.format_metric("Deals Closed", str(volumes.get('closed', 0)))
        
        # Funnel health indicators
        content += "\n**Funnel Health Indicators:**\n"
        health = funnel_data.get('health', {})
        
        # Pipeline coverage
        coverage = health.get('pipeline_coverage', 3.0)
        coverage_status = "✅" if coverage >= 3.0 else "🟡" if coverage >= 2.5 else "🔴"
        content += f"- Pipeline Coverage: {coverage:.1f}x quota {coverage_status}\n"
        
        # Stage distribution
        stage_distribution = health.get('stage_distribution', {})
        content += f"- Early Stage (Discovery): {stage_distribution.get('early', 40)}%\n"
        content += f"- Mid Stage (Technical/Business): {stage_distribution.get('mid', 35)}%\n"
        content += f"- Late Stage (Negotiation): {stage_distribution.get('late', 25)}%\n"
        
        # Velocity by stage
        content += "\n**Stage Velocity Analysis:**\n"
        velocity = funnel_data.get('velocity', {})
        for stage, days in velocity.items():
            content += f"- {stage.title()}: {days} days average\n"
        
        return content
    
    def _analyze_tool_utilization(self, context: Dict[str, Any]) -> str:
        tool_data = context.get('tool_utilization', {})
        
        content = "### Sales Tool Adoption & ROI\n\n"
        
        # Tool adoption rates
        content += "**Tool Adoption Rates:**\n"
        adoption_rates = tool_data.get('adoption_rates', {})
        
        tools = {
            'CRM (Salesforce)': adoption_rates.get('crm', 95),
            'Email Tracking': adoption_rates.get('email_tracking', 88),
            'Video Conferencing': adoption_rates.get('video_conf', 92),
            'Social Selling Tools': adoption_rates.get('social_selling', 65),
            'Proposal Software': adoption_rates.get('proposal_software', 78)
        }
        
        for tool, rate in tools.items():
            status = "✅" if rate >= 90 else "🟡" if rate >= 75 else "🔴"
            content += f"- {tool}: {rate}% {status}\n"
        
        # Usage patterns
        content += "\n**Usage Patterns:**\n"
        usage_data = tool_data.get('usage_patterns', {})
        content += self.format_metric("Daily CRM Logins", f"{usage_data.get('daily_crm_logins', 85)}%")
        content += self.format_metric("Email Templates Used", f"{usage_data.get('email_template_usage', 72)}%")
        content += self.format_metric("Call Recording Compliance", f"{usage_data.get('call_recording', 81)}%")
        content += self.format_metric("Pipeline Review Participation", f"{usage_data.get('pipeline_reviews', 88)}%")
        
        # ROI analysis
        content += "\n**Tool ROI Analysis:**\n"
        roi_data = tool_data.get('roi_analysis', {})
        
        content += f"- Email Automation: {roi_data.get('email_automation_roi', 250)}% ROI\n"
        content += f"- CRM Investment: {roi_data.get('crm_roi', 180)}% ROI\n"
        content += f"- Sales Intelligence: {roi_data.get('sales_intel_roi', 220)}% ROI\n"
        
        # Training needs
        content += "\n**Training & Support Needs:**\n"
        training_needs = tool_data.get('training_needs', [])
        if training_needs:
            for need in training_needs:
                tool = need.get('tool', 'Unknown')
                users_needing = need.get('users_needing_training', 0)
                content += f"- {tool}: {users_needing} users need additional training\n"
        else:
            content += "- ✅ No immediate training needs identified\n"
        
        return content
    
    def _generate_optimization_recommendations(self, context: Dict[str, Any]) -> str:
        content = "### Process Optimization Recommendations\n\n"
        
        recommendations = []
        
        # Based on process efficiency
        process_data = context.get('process_data', {})
        bottlenecks = process_data.get('bottlenecks', [])
        if bottlenecks:
            high_impact_bottlenecks = [b for b in bottlenecks if b.get('impact') == 'High']
            if high_impact_bottlenecks:
                recommendations.append({
                    'priority': 'High',
                    'area': 'Process Efficiency',
                    'recommendation': 'Address high-impact bottlenecks',
                    'details': f"Focus on {', '.join([b.get('stage') for b in high_impact_bottlenecks])} stages",
                    'expected_impact': 'Reduce sales cycle by 15-20%'
                })
        
        # Based on data quality
        data_quality = context.get('data_quality', {})
        overall_score = data_quality.get('overall_score', 85)
        if overall_score < 85:
            recommendations.append({
                'priority': 'High',
                'area': 'Data Quality',
                'recommendation': 'Implement data hygiene program',
                'details': 'Focus on contact completeness and activity logging',
                'expected_impact': 'Improve forecast accuracy by 10%'
            })
        
        # Based on forecast accuracy
        forecast_data = context.get('forecast_data', {})
        accuracy_issues = len(forecast_data.get('issues', []))
        if accuracy_issues > 3:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Forecast Accuracy',
                'recommendation': 'Standardize forecast methodology',
                'details': 'Implement MEDDPICC qualification rigor',
                'expected_impact': 'Increase forecast accuracy by 5-8%'
            })
        
        # Based on conversion funnel
        funnel_data = context.get('funnel_data', {})
        conversions = funnel_data.get('conversions', {})
        demo_to_proposal = conversions.get('demo_to_proposal', 45)
        if demo_to_proposal < 40:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Conversion Optimization',
                'recommendation': 'Improve demo-to-proposal conversion',
                'details': 'Enhance demo scripts and follow-up processes',
                'expected_impact': 'Increase conversion rate by 10-15%'
            })
        
        # Based on tool utilization
        tool_data = context.get('tool_utilization', {})
        adoption_rates = tool_data.get('adoption_rates', {})
        social_adoption = adoption_rates.get('social_selling', 65)
        if social_adoption < 70:
            recommendations.append({
                'priority': 'Low',
                'area': 'Tool Adoption',
                'recommendation': 'Increase social selling tool usage',
                'details': 'Provide training and success metrics tracking',
                'expected_impact': 'Improve lead generation by 20%'
            })
        
        # Format recommendations
        if recommendations:
            priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
            recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
            
            for i, rec in enumerate(recommendations, 1):
                priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(rec['priority'], '⚫')
                content += f"**{i}. {priority_emoji} {rec['recommendation']}**\n"
                content += f"   - Area: {rec['area']}\n"
                content += f"   - Priority: {rec['priority']}\n"
                content += f"   - Details: {rec['details']}\n"
                content += f"   - Expected Impact: {rec['expected_impact']}\n\n"
        else:
            content += "✅ No immediate process optimizations needed - systems running efficiently!\n"
        
        # Strategic initiatives
        content += "### Strategic Process Initiatives\n"
        content += "- **Sales Methodology Implementation**: Roll out MEDDPICC across all deals >$50K\n"
        content += "- **AI/ML Integration**: Implement predictive analytics for lead scoring\n"
        content += "- **Cross-functional Alignment**: Improve handoffs between sales and customer success\n"
        content += "- **Competitive Intelligence**: Automate competitor tracking and battlecard updates\n"
        
        return content