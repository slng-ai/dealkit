from .base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class CFOReport(BaseReport):
    """Chief Financial Officer Report - Financial outcomes and revenue expectations"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Revenue Summary
        report += self.format_section(
            "Revenue Impact",
            self._generate_revenue_summary(context)
        )
        
        # Deal Economics
        report += self.format_section(
            "Deal Economics",
            self._analyze_deal_economics(context)
        )
        
        # Financial Metrics
        report += self.format_section(
            "Key Financial Metrics",
            self._calculate_financial_metrics(context)
        )
        
        # Pipeline Contribution
        report += self.format_section(
            "Pipeline & Forecast Impact",
            self._analyze_pipeline_impact(context)
        )
        
        # Cost Analysis
        report += self.format_section(
            "Customer Acquisition Cost Analysis",
            self._analyze_cac(context)
        )
        
        # Revenue Recognition
        report += self.format_section(
            "Revenue Recognition Timeline",
            self._analyze_revenue_recognition(context)
        )
        
        # Financial Risks
        report += self.format_section(
            "Financial Risk Assessment",
            self._identify_financial_risks(context)
        )
        
        return report
    
    def _generate_revenue_summary(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Deal Value Overview\n\n"
        
        # Core metrics
        deal_size = customer_data.get('deal_size', 0)
        content += self.format_metric("Annual Contract Value (ACV)", self._format_currency(deal_size), "💵")
        content += self.format_metric("Total Contract Value (TCV)", self._format_currency(deal_size * 3), "💰")
        content += self.format_metric("Monthly Recurring Revenue (MRR)", self._format_currency(deal_size / 12), "📈")
        
        # Deal type
        deal_type = "New Business" if customer_data.get('status') != 'customer' else "Expansion"
        content += self.format_metric("Deal Type", deal_type)
        
        # Expected close quarter
        close_quarter = self._calculate_close_quarter(customer_data)
        content += self.format_metric("Expected Close Quarter", close_quarter)
        
        # Win probability impact
        win_prob = self._calculate_win_probability(customer_data, context)
        weighted_value = deal_size * (win_prob / 100)
        content += self.format_metric("Weighted Pipeline Value", self._format_currency(weighted_value))
        
        return content
    
    def _analyze_deal_economics(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        deal_size = customer_data.get('deal_size', 0)
        
        content = "### Deal Structure & Terms\n\n"
        
        # Payment terms
        content += "**Payment Structure:**\n"
        content += "- Payment Terms: Net 30 (standard)\n"
        content += "- Billing Frequency: Annual upfront / Quarterly\n"
        content += "- Contract Length: 12 months (auto-renewal)\n\n"
        
        # Pricing model
        content += "**Pricing Model:**\n"
        content += "- Base Platform Fee: $X/month\n"
        content += "- Usage-Based Component: $Y per 1M inferences\n"
        content += "- Professional Services: $Z one-time\n\n"
        
        # Discount analysis
        content += "**Discount Analysis:**\n"
        list_price = deal_size * 1.2  # Assume 20% discount
        discount_amount = list_price - deal_size
        discount_percent = (discount_amount / list_price) * 100
        
        content += self.format_metric("List Price", self._format_currency(list_price))
        content += self.format_metric("Negotiated Price", self._format_currency(deal_size))
        content += self.format_metric("Discount", f"{discount_percent:.1f}% ({self._format_currency(discount_amount)})")
        
        # Margin analysis
        content += "\n**Gross Margin Analysis:**\n"
        gross_margin = deal_size * 0.8  # Assume 80% gross margin
        content += self.format_metric("Gross Margin", f"80% ({self._format_currency(gross_margin)})")
        content += self.format_metric("Infrastructure Costs", self._format_currency(deal_size * 0.15))
        content += self.format_metric("Support Costs", self._format_currency(deal_size * 0.05))
        
        return content
    
    def _calculate_financial_metrics(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        deal_size = customer_data.get('deal_size', 0)
        
        content = "### Financial Performance Indicators\n\n"
        
        # LTV calculation
        churn_rate = 0.1  # 10% annual churn assumption
        ltv = deal_size / churn_rate
        content += self.format_metric("Estimated LTV", self._format_currency(ltv), "📈")
        
        # Payback period
        cac = self._calculate_cac_amount(customer_data)
        payback_months = (cac / (deal_size / 12)) if deal_size > 0 else 0
        content += self.format_metric("CAC Payback Period", f"{payback_months:.1f} months")
        
        # LTV:CAC ratio
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        ratio_health = "✅" if ltv_cac_ratio >= 3 else "⚠️" if ltv_cac_ratio >= 2 else "🔴"
        content += self.format_metric("LTV:CAC Ratio", f"{ltv_cac_ratio:.1f}:1 {ratio_health}")
        
        # Magic number (net new ARR / S&M spend)
        magic_number = (deal_size * 4) / (cac * 4)  # Quarterly view
        content += self.format_metric("Magic Number", f"{magic_number:.2f}")
        
        # Rule of 40
        growth_rate = 50  # Assumed growth rate
        profit_margin = 20  # Assumed profit margin
        rule_of_40 = growth_rate + profit_margin
        content += self.format_metric("Rule of 40 Score", f"{rule_of_40} (Growth: {growth_rate}% + Margin: {profit_margin}%)")
        
        return content
    
    def _analyze_pipeline_impact(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        deal_size = customer_data.get('deal_size', 0)
        
        content = "### Forecast & Pipeline Contribution\n\n"
        
        # Current quarter impact
        current_quarter = self._get_current_quarter()
        close_quarter = self._calculate_close_quarter(customer_data)
        
        if close_quarter == current_quarter:
            content += f"🎯 **In-Quarter Deal** - Critical for {current_quarter} target\n\n"
        else:
            content += f"📅 **Future Quarter Deal** - Targeting {close_quarter}\n\n"
        
        # Pipeline metrics
        win_prob = self._calculate_win_probability(customer_data, context)
        content += "**Pipeline Metrics:**\n"
        content += self.format_metric("Pipeline Stage", customer_data.get('stage', 'Unknown').title())
        content += self.format_metric("Win Probability", f"{win_prob}%")
        content += self.format_metric("Weighted Value", self._format_currency(deal_size * win_prob / 100))
        content += self.format_metric("Days to Close", self._calculate_days_to_close(customer_data))
        
        # Forecast categories
        content += "\n**Forecast Category:**\n"
        forecast_cat = self._determine_forecast_category(customer_data, win_prob)
        cat_emoji = {
            'Closed': '🎉',
            'Commit': '✅',
            'Best Case': '🟡',
            'Pipeline': '🟠',
            'Omitted': '🔴'
        }.get(forecast_cat, '❓')
        content += f"{cat_emoji} **{forecast_cat}**\n\n"
        
        # Quarter contribution
        quarterly_target = 5000000  # $5M quarterly target
        contribution_percent = (deal_size / quarterly_target) * 100
        content += self.format_metric("Quarter Contribution", f"{contribution_percent:.1f}% of target")
        
        return content
    
    def _analyze_cac(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Customer Acquisition Cost Breakdown\n\n"
        
        # Calculate CAC components
        cac_breakdown = self._calculate_cac_breakdown(customer_data)
        
        total_cac = sum(cac_breakdown.values())
        content += self.format_metric("Total CAC", self._format_currency(total_cac), "📊")
        
        content += "\n**CAC Components:**\n"
        for component, cost in cac_breakdown.items():
            percentage = (cost / total_cac * 100) if total_cac > 0 else 0
            content += f"- {component}: {self._format_currency(cost)} ({percentage:.0f}%)\n"
        
        # Efficiency metrics
        content += "\n**Sales Efficiency:**\n"
        deal_size = customer_data.get('deal_size', 0)
        sales_efficiency = deal_size / total_cac if total_cac > 0 else 0
        content += self.format_metric("Sales Efficiency Ratio", f"{sales_efficiency:.2f}x")
        
        # Time to productivity
        days_in_pipeline = self._calculate_days_in_pipeline(customer_data)
        content += self.format_metric("Sales Cycle Length", f"{days_in_pipeline} days")
        
        # Benchmark comparison
        content += "\n**Benchmark Comparison:**\n"
        industry_avg_cac = deal_size * 0.15  # 15% of ACV
        delta = total_cac - industry_avg_cac
        if delta > 0:
            content += f"⚠️ CAC is {self._format_currency(abs(delta))} above industry average\n"
        else:
            content += f"✅ CAC is {self._format_currency(abs(delta))} below industry average\n"
        
        return content
    
    def _analyze_revenue_recognition(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        deal_size = customer_data.get('deal_size', 0)
        
        content = "### Revenue Recognition Schedule\n\n"
        
        # Recognition timeline
        close_date = self._calculate_close_date(customer_data)
        content += self.format_metric("Expected Close Date", close_date.strftime('%Y-%m-%d'))
        content += self.format_metric("Revenue Start Date", (close_date + timedelta(days=30)).strftime('%Y-%m-%d'))
        
        # Monthly recognition
        content += "\n**Monthly Revenue Recognition:**\n"
        monthly_revenue = deal_size / 12
        
        for i in range(12):
            month_date = close_date + timedelta(days=30*(i+1))
            quarter = f"Q{(month_date.month-1)//3 + 1} {month_date.year}"
            if i < 3:
                content += f"- {month_date.strftime('%B %Y')}: {self._format_currency(monthly_revenue)} ({quarter})\n"
        content += f"- ... continuing for 12 months total\n"
        
        # Quarterly summary
        content += "\n**Quarterly Revenue Impact:**\n"
        for q in range(4):
            q_revenue = monthly_revenue * 3
            quarter_num = ((close_date.month-1)//3 + 1 + q) % 4 + 1
            year = close_date.year + ((close_date.month-1)//3 + 1 + q) // 4
            content += f"- Q{quarter_num} {year}: {self._format_currency(q_revenue)}\n"
        
        # Deferred revenue
        content += "\n**Balance Sheet Impact:**\n"
        content += self.format_metric("Initial Deferred Revenue", self._format_currency(deal_size))
        content += self.format_metric("Monthly Revenue Recognition", self._format_currency(monthly_revenue))
        
        return content
    
    def _identify_financial_risks(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Financial Risk Factors\n\n"
        
        risks = []
        
        # Collection risk
        if not customer_data.get('assessment', {}).get('budget_confirmed'):
            risks.append({
                'risk': 'Budget Not Confirmed',
                'impact': 'High',
                'description': 'No formal budget approval - risk of deal pushout or reduction',
                'mitigation': 'Get written budget confirmation from CFO/procurement'
            })
        
        # Concentration risk
        deal_size = customer_data.get('deal_size', 0)
        if deal_size > 500000:  # Large deal
            risks.append({
                'risk': 'Customer Concentration',
                'impact': 'Medium',
                'description': 'Large deal increases revenue concentration risk',
                'mitigation': 'Ensure strong contract terms and expansion opportunities'
            })
        
        # Payment terms risk
        if customer_data.get('payment_terms') == 'quarterly':
            risks.append({
                'risk': 'Cash Flow Impact',
                'impact': 'Medium',
                'description': 'Quarterly payments affect cash collection timing',
                'mitigation': 'Negotiate annual upfront payment with discount'
            })
        
        # Competition risk
        if customer_data.get('assessment', {}).get('competition'):
            risks.append({
                'risk': 'Competitive Pressure',
                'impact': 'High',
                'description': 'Active competition may force pricing concessions',
                'mitigation': 'Emphasize ROI and unique value propositions'
            })
        
        # Format risks
        for risk in risks:
            impact_emoji = "🔴" if risk['impact'] == 'High' else "🟡"
            content += f"**{impact_emoji} {risk['risk']}**\n"
            content += f"- Impact: {risk['impact']}\n"
            content += f"- Description: {risk['description']}\n"
            content += f"- Mitigation: {risk['mitigation']}\n\n"
        
        if not risks:
            content += "✅ No significant financial risks identified\n"
        
        # Credit assessment
        content += "### Credit & Payment Risk\n"
        content += "- **Credit Check Status:** ❓ Pending\n"
        content += "- **D&B Rating:** ❓ To be verified\n"
        content += "- **Payment History:** New customer\n"
        content += "- **Recommended Terms:** Net 30, annual upfront\n"
        
        return content
    
    # Helper methods
    def _load_customer_data(self, customer_id: str) -> Dict[str, Any]:
        try:
            with open(f'customers/{customer_id}.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _format_currency(self, amount: float) -> str:
        if amount >= 1000000:
            return f"${amount/1000000:.2f}M"
        elif amount >= 1000:
            return f"${amount/1000:.0f}K"
        else:
            return f"${amount:.0f}"
    
    def _calculate_close_quarter(self, customer_data: Dict[str, Any]) -> str:
        close_date = self._calculate_close_date(customer_data)
        quarter = (close_date.month - 1) // 3 + 1
        return f"Q{quarter} {close_date.year}"
    
    def _calculate_close_date(self, customer_data: Dict[str, Any]) -> datetime:
        # Use expected close date or calculate based on stage
        if customer_data.get('expected_close_date'):
            return datetime.fromisoformat(customer_data['expected_close_date'])
        
        # Estimate based on stage
        stage = customer_data.get('stage', 'discovery')
        days_to_close = {
            'discovery': 60,
            'technical_validation': 45,
            'business_case': 30,
            'negotiation': 14,
            'closed_won': 0
        }.get(stage.lower(), 60)
        
        return datetime.now() + timedelta(days=days_to_close)
    
    def _calculate_win_probability(self, customer_data: Dict[str, Any], context: Dict[str, Any]) -> int:
        # Reuse CRO logic
        stage_probs = {
            'discovery': 20,
            'technical_validation': 40,
            'business_case': 65,
            'negotiation': 85,
            'closed_won': 100
        }
        return stage_probs.get(customer_data.get('stage', 'discovery').lower(), 20)
    
    def _calculate_cac_amount(self, customer_data: Dict[str, Any]) -> float:
        # Simplified CAC calculation
        deal_size = customer_data.get('deal_size', 0)
        return deal_size * 0.2  # Assume 20% of ACV
    
    def _get_current_quarter(self) -> str:
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        return f"Q{quarter} {now.year}"
    
    def _calculate_days_to_close(self, customer_data: Dict[str, Any]) -> str:
        close_date = self._calculate_close_date(customer_data)
        days = (close_date - datetime.now()).days
        return f"{max(0, days)} days"
    
    def _determine_forecast_category(self, customer_data: Dict[str, Any], win_prob: int) -> str:
        stage = customer_data.get('stage', 'discovery')
        
        if stage == 'closed_won':
            return 'Closed'
        elif stage == 'negotiation' and win_prob >= 80:
            return 'Commit'
        elif stage in ['business_case', 'negotiation'] and win_prob >= 60:
            return 'Best Case'
        elif win_prob >= 20:
            return 'Pipeline'
        else:
            return 'Omitted'
    
    def _calculate_cac_breakdown(self, customer_data: Dict[str, Any]) -> Dict[str, float]:
        deal_size = customer_data.get('deal_size', 0)
        
        # Estimate CAC components
        return {
            'Sales Salary & Commission': deal_size * 0.10,
            'Marketing Attribution': deal_size * 0.05,
            'Sales Engineering': deal_size * 0.03,
            'Tools & Systems': deal_size * 0.01,
            'Management Overhead': deal_size * 0.01
        }
    
    def _calculate_days_in_pipeline(self, customer_data: Dict[str, Any]) -> int:
        created = customer_data.get('created_at')
        if created:
            created_date = datetime.fromisoformat(created)
            return (datetime.now() - created_date).days
        return 0